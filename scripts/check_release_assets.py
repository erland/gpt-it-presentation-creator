"""Project-specific check of canonical output, including separate Engine."""
import hashlib,json,os,subprocess,sys,tempfile,zipfile
from pathlib import Path
import yaml
root=Path(__file__).resolve().parents[1]; dist=root/'dist'
cfg=yaml.safe_load((root/'gpt-project.yaml').read_text()); m=json.loads((dist/'DELIVERY-MANIFEST.json').read_text()); version=m['version']; pid=cfg['project']['id']
expected={f'{pid}-{name}-{version}.zip' for name in ('project','chat','claude-project','claude-skills','opencode','plugin','engine')}
assert {p.name for p in dist.glob('*.zip')}==expected
assert {a['file'] for a in m['artifacts']}==expected|{'SHA256SUMS.txt'}
for a in m['artifacts']:
 p=dist/a['file']; assert p.stat().st_size==a['size']; assert hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256']
checks=dict(line.split()[::-1] for line in (dist/'SHA256SUMS.txt').read_text().splitlines()); assert set(checks)==expected
for name in expected:
 p=dist/name; assert hashlib.sha256(p.read_bytes()).hexdigest()==checks[name]
 with zipfile.ZipFile(p) as z: assert z.testzip() is None
with zipfile.ZipFile(dist/f'{pid}-project-{version}.zip') as z:
 assert {'.github/workflows/ci.yml','.github/workflows/release.yml','scripts/check_release_assets.py'}<=set(z.namelist())
with tempfile.TemporaryDirectory() as d:
 with zipfile.ZipFile(dist/f'{pid}-engine-{version}.zip') as z: z.extractall(d)
 p=Path(d); manifest=json.loads((p/'engine-package.json').read_text()); print('Engine manifest:',manifest.keys())
 for name, digest in manifest['files'].items():
  assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest
 subprocess.run([sys.executable,str(p/cfg['engine']['selftest'])],check=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
print('PASS: seven canonical archives, manifest, SHA256, project workflows and extracted engine self-test')
