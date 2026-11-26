"""DEV-013: independently verify distribution version, Engine contract, SHA256 and release readiness.

This is a technical release-candidate gate, not a claim of visual or host acceptance.
"""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

import yaml

TARGETS=('project','chat','claude-project','claude-skills','opencode','plugin','engine')
RUNTIMES=TARGETS[1:-1]
VERSION=re.compile(r'^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?
SHA256=re.compile(r'^[0-9a-f]{64}$')


def verify(root: Path, version: str) -> dict:
    if not VERSION.fullmatch(version) or '+' in version:
        raise ValueError(f'Invalid candidate version: {version}')
    cfg=yaml.safe_load((root/'gpt-project.yaml').read_text(encoding='utf-8'))
    pid=cfg['project']['id']
    dist=root/'dist'
    manifest=json.loads((dist/'DELIVERY-MANIFEST.json').read_text(encoding='utf-8'))
    if manifest['version']!=version:
        raise ValueError('Delivery manifest version does not match candidate tag')
    expected={f'{pid}-{target}-{version}.zip' for target in TARGETS}
    actual={p.name for p in dist.glob('*.zip')}
    if actual != expected:
        raise ValueError(f'Unexpected archive set: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}')
    listed={record['file']:record for record in manifest['artifacts']}
    if set(listed) != expected|{'SHA256SUMS.txt'}:
        raise ValueError('Delivery manifest artifact list differs from canonical seven archives')
    checksum_lines=(dist/'SHA256SUMS.txt').read_text().splitlines()
    checksums={}
    for line in checksum_lines:
        digest,name=line.split()
        if not SHA256.fullmatch(digest) or name in checksums:
            raise ValueError('Malformed or duplicate SHA256 entry')
        checksums[name]=digest
    if set(checksums)!=expected: raise ValueError('Incomplete checksum list')
    check_file=dist/'SHA256SUMS.txt'
    if (hashlib.sha256(check_file.read_bytes()).hexdigest()!=listed['SHA256SUMS.txt']['sha256']
            or check_file.stat().st_size!=listed['SHA256SUMS.txt']['size']):
        raise ValueError('Checksum-list integrity mismatch')
    result={'schema_version':1,'version':version,'technical_status':'pass',
            'host_acceptance':'not_run','visual_acceptance':'not_verified_in_powerpoint',
            'artifacts':[],'engine':{},'runtime_parity':{}}
    engine_icon_hash=None
    for filename in sorted(expected):
        path=dist/filename
        actual_hash=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash!=checksums[filename] or actual_hash!=listed[filename]['sha256']:
            raise ValueError(f'Checksum mismatch: {filename}')
        if path.stat().st_size!=listed[filename]['size']:
            raise ValueError(f'Size mismatch: {filename}')
        with zipfile.ZipFile(path) as z:
            if z.testzip() is not None:raise ValueError(f'Invalid archive: {filename}')
            names=z.namelist()
            if len(names)!=len(set(names)):raise ValueError(f'Duplicate ZIP entries: {filename}')
            if any(name.startswith('/') or '..' in Path(name).parts for name in names):
                raise ValueError(f'Unsafe ZIP entry: {filename}')
            if '-engine-' in filename:
                data=json.loads(z.read('engine-package.json'))
                if data['version']!=version or data['engine_id']!=pid:
                    raise ValueError('Wrong Engine version or identity')
                if data['entrypoint'] not in data['files']:
                    raise ValueError('Engine entrypoint missing')
                if not set(data['required_files'])<=set(data['files']):
                    raise ValueError('Engine required file missing')
                for item,digest in data['files'].items():
                    if hashlib.sha256(z.read(item)).hexdigest()!=digest:
                        raise ValueError(f'Engine source hash mismatch: {item}')
                icon_files=[item for item in data['files'] if item.endswith('/professional-icons.yaml')]
                if len(icon_files)!=1:raise ValueError('Engine professional icon registry missing')
                engine_icon_hash=data['files'][icon_files[0]]
                result['engine']={'version':data['version'],'entrypoint':data['entrypoint'],
                                  'file_count':len(data['files'])}
            else:
                version_entries=[name for name in names if name=='VERSION' or name.endswith('/VERSION')]
                manifest_entries=[name for name in names if name=='MANIFEST.json' or name.endswith('/MANIFEST.json')]
                if '-project-' not in filename:
                    if not version_entries or not manifest_entries:
                        raise ValueError(f'Runtime VERSION/MANIFEST missing: {filename}')
                    if any(z.read(x).decode().strip()!=version for x in version_entries):
                        raise ValueError(f'Runtime version mismatch: {filename}')
                    if any(json.loads(z.read(x))['version']!=version for x in manifest_entries):
                        raise ValueError(f'Runtime manifest version mismatch: {filename}')
            result['artifacts'].append({'file':filename,'sha256':actual_hash,
                                        'bytes':path.stat().st_size,'entries':len(names)})
    for runtime in RUNTIMES:
        filename=f'{pid}-{runtime}-{version}.zip'
        with zipfile.ZipFile(dist/filename) as z:
            icons=tuple(sorted(x for x in z.namelist() if x.endswith('/professional-icons.yaml')))
            if not icons:raise ValueError(f'Icon resources missing in {runtime}')
            hashes={hashlib.sha256(z.read(p)).hexdigest() for p in icons}
            if len(hashes)!=1:raise ValueError(f'Inconsistent icon resources within {runtime}')
            result['runtime_parity'][runtime]=next(iter(hashes))
    if len(set(result['runtime_parity'].values()))!=1:
        raise ValueError('Professional icons differ across runtime distributions')
    if next(iter(result['runtime_parity'].values())) != engine_icon_hash:
        raise ValueError('Professional icons differ between Engine and runtime distributions')
    engine_file=next(x for x in result['artifacts'] if '-engine-' in x['file'])
    result['engine']['archive_sha256']=engine_file['sha256']
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--project-root',type=Path,default=Path('.'))
    parser.add_argument('--version',required=True)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=verify(args.project_root,args.version)
    payload=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding='utf-8')
    print(f'PASS: candidate {args.version}; seven ZIPs, SHA256, Engine identity and five-runtime icon parity')


if __name__=='__main__':
    main()
)
SHA256=re.compile(r'^[0-9a-f]{64}$')


def verify(root: Path, version: str) -> dict:
    if not VERSION.fullmatch(version) or '+' in version:
        raise ValueError(f'Invalid candidate version: {version}')
    cfg=yaml.safe_load((root/'gpt-project.yaml').read_text(encoding='utf-8'))
    pid=cfg['project']['id']
    dist=root/'dist'
    manifest=json.loads((dist/'DELIVERY-MANIFEST.json').read_text(encoding='utf-8'))
    if manifest['version']!=version:
        raise ValueError('Delivery manifest version does not match candidate tag')
    expected={f'{pid}-{target}-{version}.zip' for target in TARGETS}
    actual={p.name for p in dist.glob('*.zip')}
    if actual != expected:
        raise ValueError(f'Unexpected archive set: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}')
    listed={record['file']:record for record in manifest['artifacts']}
    if set(listed) != expected|{'SHA256SUMS.txt'}:
        raise ValueError('Delivery manifest artifact list differs from canonical seven archives')
    checksum_lines=(dist/'SHA256SUMS.txt').read_text().splitlines()
    checksums={}
    for line in checksum_lines:
        digest,name=line.split()
        if not SHA256.fullmatch(digest) or name in checksums:
            raise ValueError('Malformed or duplicate SHA256 entry')
        checksums[name]=digest
    if set(checksums)!=expected: raise ValueError('Incomplete checksum list')
    check_file=dist/'SHA256SUMS.txt'
    if (hashlib.sha256(check_file.read_bytes()).hexdigest()!=listed['SHA256SUMS.txt']['sha256']
            or check_file.stat().st_size!=listed['SHA256SUMS.txt']['size']):
        raise ValueError('Checksum-list integrity mismatch')
    result={'schema_version':1,'version':version,'technical_status':'pass',
            'host_acceptance':'not_run','visual_acceptance':'not_verified_in_powerpoint',
            'artifacts':[],'engine':{},'runtime_parity':{}}
    engine_icon_hash=None
    for filename in sorted(expected):
        path=dist/filename
        actual_hash=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash!=checksums[filename] or actual_hash!=listed[filename]['sha256']:
            raise ValueError(f'Checksum mismatch: {filename}')
        if path.stat().st_size!=listed[filename]['size']:
            raise ValueError(f'Size mismatch: {filename}')
        with zipfile.ZipFile(path) as z:
            if z.testzip() is not None:raise ValueError(f'Invalid archive: {filename}')
            names=z.namelist()
            if len(names)!=len(set(names)):raise ValueError(f'Duplicate ZIP entries: {filename}')
            if any(name.startswith('/') or '..' in Path(name).parts for name in names):
                raise ValueError(f'Unsafe ZIP entry: {filename}')
            if '-engine-' in filename:
                data=json.loads(z.read('engine-package.json'))
                if data['version']!=version or data['engine_id']!=pid:
                    raise ValueError('Wrong Engine version or identity')
                if data['entrypoint'] not in data['files']:
                    raise ValueError('Engine entrypoint missing')
                if not set(data['required_files'])<=set(data['files']):
                    raise ValueError('Engine required file missing')
                for item,digest in data['files'].items():
                    if hashlib.sha256(z.read(item)).hexdigest()!=digest:
                        raise ValueError(f'Engine source hash mismatch: {item}')
                icon_files=[item for item in data['files'] if item.endswith('/professional-icons.yaml')]
                if len(icon_files)!=1:raise ValueError('Engine professional icon registry missing')
                engine_icon_hash=data['files'][icon_files[0]]
                result['engine']={'version':data['version'],'entrypoint':data['entrypoint'],
                                  'file_count':len(data['files'])}
            else:
                version_entries=[name for name in names if name=='VERSION' or name.endswith('/VERSION')]
                manifest_entries=[name for name in names if name=='MANIFEST.json' or name.endswith('/MANIFEST.json')]
                if '-project-' not in filename:
                    if not version_entries or not manifest_entries:
                        raise ValueError(f'Runtime VERSION/MANIFEST missing: {filename}')
                    if any(z.read(x).decode().strip()!=version for x in version_entries):
                        raise ValueError(f'Runtime version mismatch: {filename}')
                    if any(json.loads(z.read(x))['version']!=version for x in manifest_entries):
                        raise ValueError(f'Runtime manifest version mismatch: {filename}')
            result['artifacts'].append({'file':filename,'sha256':actual_hash,
                                        'bytes':path.stat().st_size,'entries':len(names)})
    for runtime in RUNTIMES:
        filename=f'{pid}-{runtime}-{version}.zip'
        with zipfile.ZipFile(dist/filename) as z:
            icons=tuple(sorted(x for x in z.namelist() if x.endswith('/professional-icons.yaml')))
            if not icons:raise ValueError(f'Icon resources missing in {runtime}')
            hashes={hashlib.sha256(z.read(p)).hexdigest() for p in icons}
            if len(hashes)!=1:raise ValueError(f'Inconsistent icon resources within {runtime}')
            result['runtime_parity'][runtime]=next(iter(hashes))
    if len(set(result['runtime_parity'].values()))!=1:
        raise ValueError('Professional icons differ across runtime distributions')
    if next(iter(result['runtime_parity'].values())) != engine_icon_hash:
        raise ValueError('Professional icons differ between Engine and runtime distributions')
    engine_file=next(x for x in result['artifacts'] if '-engine-' in x['file'])
    result['engine']['archive_sha256']=engine_file['sha256']
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--project-root',type=Path,default=Path('.'))
    parser.add_argument('--version',required=True)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=verify(args.project_root,args.version)
    payload=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding='utf-8')
    print(f'PASS: candidate {args.version}; seven ZIPs, SHA256, Engine identity and five-runtime icon parity')


if __name__=='__main__':
    main()
