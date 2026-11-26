"""Project-specific check of canonical output, including separate Engine."""
import hashlib,json,os,subprocess,sys,tempfile,zipfile
from pathlib import Path
import yaml
root=Path(__file__).resolve().parents[1]; dist=root/'dist'
cfg=yaml.safe_load((root/'gpt-project.yaml').read_text()); m=json.loads((dist/'DELIVERY-MANIFEST.json').read_text()); version=m['version']; pid=cfg['project']['id']
expected={f'{pid}-{name}-{version}.zip' for name in ('project','chat','claude-project','claude-skills','opencode','plugin','engine')}
assert {p.name for p in dist.glob('*.zip')}==expected
assert {a['file'] for a in m['artifacts']}==expected|{'SHA256SUMS.txt'}
# DEV-013: prevent releasing mismatched, empty, or unreproducibly versioned packages.
assert m['version']==version
assert len(m['artifacts'])==8 and len({a['file'] for a in m['artifacts']})==8
assert all(a['size']>100 for a in m['artifacts'])
for target in ('chat','claude-project','claude-skills','opencode','plugin'):
 with zipfile.ZipFile(dist/f'{pid}-{target}-{version}.zip') as z:
  names=z.namelist()
  versions=[name for name in names if name=='VERSION' or name.endswith('/VERSION')]
  assert versions, (target,'missing VERSION')
  assert all(z.read(name).decode('utf-8').strip()==version for name in versions), (target,versions)
  manifest_names=[name for name in names if name=='MANIFEST.json' or name.endswith('/MANIFEST.json')]
  assert manifest_names, (target,'missing MANIFEST')
  assert all(json.loads(z.read(name))['version']==version for name in manifest_names), (target,'manifest version')

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

# DEV-010: every generated instruction projection must retain the core gate.
for target in ('chat','claude-project','claude-skills','opencode','plugin'):
 with zipfile.ZipFile(dist/f'{pid}-{target}-{version}.zip') as z:
  names=[n for n in z.namelist() if n.endswith(('/SKILL.md','/instructions.md')) or n=='AGENTS.md']
  assert names, target
  if target=='opencode':
   assert 'AGENTS.md' in names
   skills=[n for n in names if n.endswith('/SKILL.md')]
   assert len(skills)==len(cfg['skills']['definitions'])
   for name in skills:
    assert 'Följ obligatorisk Engine-preflight' in z.read(name).decode('utf-8'), (target,name)
   names=['AGENTS.md']
  for name in names:
   instruction=z.read(name).decode('utf-8')
   assert 'Ingen automatisk fallback' in instruction, (target,name)
   assert 'invänta uppladdning' in instruction, (target,name)
   assert 'uttryckligt användargodkännande' in instruction, (target,name)
   assert 'releases/download/vVERSION/' in instruction, (target,name)
   if target=='plugin' and not (version.endswith('-ci') or version.startswith('0.0.0-')):
    assert f"https://github.com/{cfg['engine']['release_repository']}/releases/download/v{version}/{pid}-engine-{version}.zip" in instruction
print('PASS: DEV-010 canonical preflight across five runtime distributions')

# DEV-011: one activation point, explicit routing and byte-identical workflow references.
workflow_names=('presentation-design.md','powerpoint-creation.md','presentation-review.md')
for target in ('chat','claude-project','claude-skills','opencode','plugin'):
 with zipfile.ZipFile(dist/f'{pid}-{target}-{version}.zip') as z:
  names=z.namelist()
  skills=[n for n in names if n.endswith('/SKILL.md')]
  if target in ('claude-skills','opencode','plugin'):
   assert len(skills)==1 and skills[0].endswith('/it-presentation-creator/SKILL.md'), (target,skills)
  instructions=[n for n in names if n.endswith('/instructions.md') or n=='AGENTS.md' or n in skills]
  merged='\n'.join(z.read(n).decode('utf-8') for n in instructions)
  assert 'Val av arbetsflöde (DEV-011)' in merged, target
  for marker in ('Obligatorisk visuell acceptansgrind','minst två dokumenterade granskningsomgångar','leverera endast som utkast'):
   assert marker in merged, (target,marker)
  for workflow in workflow_names:
   assert workflow in merged, (target,workflow)
   matches=[n for n in names if n.endswith('/'+workflow)]
   assert matches, (target,workflow)
   expected_bytes=(root/'knowledge'/'workflows'/workflow).read_bytes()
   assert all(z.read(n)==expected_bytes for n in matches), (target,workflow)
print('PASS: one Skill and workflow parity across five runtime distributions')

# DEV-012A: both icon resources must survive every runtime and Engine projection.
for target in ('chat','claude-project','claude-skills','opencode','plugin','engine'):
 with zipfile.ZipFile(dist/f'{pid}-{target}-{version}.zip') as z:
  for filename in ('technical-icon-register.yaml','professional-icons.yaml'):
   matches=[n for n in z.namelist() if n.endswith('/'+filename)]
   assert matches, (target,filename)
   assert all(z.read(n)==(root/'knowledge/figures'/filename).read_bytes() for n in matches), (target,filename)
print('PASS: technical icon resources across runtimes and Engine')

# DEV-012A2: no retired outline catalog in any archive; selection guide in every runtime.
for name in expected:
 with zipfile.ZipFile(dist/name) as z:
  assert not any(n.endswith(('/outline-icons.yaml','/library.yaml')) for n in z.namelist()), name
  if '-engine-' not in name and '-project-' not in name:
   matches=[n for n in z.namelist() if n.endswith('/visual-selection-guide.md')]
   assert matches, name
   assert all(z.read(n)==(root/'knowledge/figures/visual-selection-guide.md').read_bytes() for n in matches), name
