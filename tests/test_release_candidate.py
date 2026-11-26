"""DEV-013: release verification is an executable gate, including failure cases."""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import pytest
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from verify_release_candidate import verify

VERSION='0.5.3-rc.1'
PID='it-presentation-creator'
TARGETS=('project','chat','claude-project','claude-skills','opencode','plugin','engine')

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write_archive(path,entries):
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in entries.items():
            if isinstance(data,str):data=data.encode()
            z.writestr(name,data)

def fixture_candidate(tmp_path,icon_override=None):
    dist=tmp_path/'dist'
    dist.mkdir()
    (tmp_path/'gpt-project.yaml').write_text(yaml.safe_dump({'project':{'id':PID}}))
    main_icon=b'icons: {}\n'
    checks={}
    rows=[]
    for target in TARGETS:
        filename=f'{PID}-{target}-{VERSION}.zip'
        path=dist/filename
        if target=='project':
            entries={'gpt-project.yaml':f'project: {PID}\n'}
        elif target=='engine':
            files={'scripts/itpc/selftest.py':b'print("engine")\n',
                   'knowledge/figures/professional-icons.yaml':main_icon}
            manifest={'version':VERSION,'engine_id':PID,'entrypoint':'scripts/itpc/selftest.py',
                      'required_files':['scripts/itpc/selftest.py'],
                      'files':{k:digest(v) for k,v in files.items()}}
            entries={**files,'engine-package.json':json.dumps(manifest)}
        else:
            icon=(b'different icons\n' if icon_override==target else main_icon)
            entries={'VERSION':VERSION+'\n',
                     'MANIFEST.json':json.dumps({'version':VERSION,'adapter_id':target}),
                     'knowledge/figures/professional-icons.yaml':icon,
                     'SKILL.md':'# Test'}
        write_archive(path,entries)
        checksum=digest(path.read_bytes())
        checks[filename]=checksum
        rows.append({'file':filename,'sha256':checksum,'size':path.stat().st_size})
    checksum_path=dist/'SHA256SUMS.txt'
    checksum_path.write_text(''.join(f'{value}  {key}\n' for key,value in sorted(checks.items())))
    rows.append({'file':'SHA256SUMS.txt','sha256':digest(checksum_path.read_bytes()),
                 'size':checksum_path.stat().st_size})
    (dist/'DELIVERY-MANIFEST.json').write_text(json.dumps({'version':VERSION,
                                                            'artifacts':rows}))
    return tmp_path

def test_candidate_gate_accepts_one_consistent_engine_and_five_runtimes(tmp_path):
    root=fixture_candidate(tmp_path)
    result=verify(root,VERSION)
    assert result['technical_status']=='pass'
    assert result['host_acceptance']=='not_run'
    assert result['visual_acceptance']=='not_verified_in_powerpoint'
    assert len(result['artifacts'])==7
    assert len(result['runtime_parity'])==5
    assert result['engine']['version']==VERSION
    assert result['engine']['file_count']==2
    assert all(len(x['sha256'])==64 for x in result['artifacts'])

@pytest.mark.parametrize('version',[
    '0.5.3+build.1','v0.5.3-rc.1','../../dist','0.5.3-rc.1--oops','0.5.3-rc.1/evil'
])
def test_candidate_gate_rejects_malformed_version(tmp_path,version):
    root=fixture_candidate(tmp_path)
    with pytest.raises(ValueError,match='Invalid candidate version|Delivery manifest version'):
        verify(root,version)

def test_candidate_gate_rejects_tampered_zip(tmp_path):
    root=fixture_candidate(tmp_path)
    archive=root/'dist'/f'{PID}-plugin-{VERSION}.zip'
    with archive.open('ab') as f:f.write(b'tamper')
    with pytest.raises(ValueError,match='Checksum mismatch'):
        verify(root,VERSION)

def test_candidate_gate_rejects_tampered_checksum_list(tmp_path):
    root=fixture_candidate(tmp_path)
    with (root/'dist'/'SHA256SUMS.txt').open('a') as f:f.write('corrupted\n')
    with pytest.raises(ValueError,match='Malformed|Checksum-list integrity'):
        verify(root,VERSION)

def test_candidate_gate_rejects_runtime_icon_drift(tmp_path):
    root=fixture_candidate(tmp_path,icon_override='opencode')
    with pytest.raises(ValueError,match='Professional icons differ'):
        verify(root,VERSION)

def test_candidate_gate_rejects_wrong_engine_identity(tmp_path):
    root=fixture_candidate(tmp_path)
    archive=root/'dist'/f'{PID}-engine-{VERSION}.zip'
    with zipfile.ZipFile(archive) as z:
        data={name:z.read(name) for name in z.namelist()}
    manifest=json.loads(data['engine-package.json'])
    manifest['engine_id']='wrong-project'
    data['engine-package.json']=json.dumps(manifest).encode()
    write_archive(archive,data)
    manifest_path=root/'dist'/'DELIVERY-MANIFEST.json'
    delivery=json.loads(manifest_path.read_text())
    for row in delivery['artifacts']:
        if row['file']==archive.name:
            row['sha256']=digest(archive.read_bytes())
            row['size']=archive.stat().st_size
    manifest_path.write_text(json.dumps(delivery))
    checks=root/'dist'/'SHA256SUMS.txt'
    lines=[f'{digest(archive.read_bytes())}  {archive.name}\n' if archive.name in line
           else line for line in checks.read_text().splitlines(keepends=True)]
    checks.write_text(''.join(lines))
    delivery['artifacts'][-1]['sha256']=digest(checks.read_bytes())
    delivery['artifacts'][-1]['size']=checks.stat().st_size
    manifest_path.write_text(json.dumps(delivery))
    with pytest.raises(ValueError,match='Wrong Engine version or identity'):
        verify(root,VERSION)
