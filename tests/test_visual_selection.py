from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def test_visual_selection():
    folder = ROOT / 'knowledge/figures'
    libraries = {
        'figure': yaml.safe_load((folder/'library.yaml').read_text())['figures'],
        'professional-icon': yaml.safe_load((folder/'professional-icons.yaml').read_text())['icons'],
    }
    guide = (folder/'visual-selection-guide.md').read_text()
    rows = [line.split('|')[1:5] for line in guide.splitlines() if line.startswith('| ') and not line.startswith('| Typ')]
    actual = set()
    for kind, key, status, reason in rows:
        kind, key, status = kind.strip(), key.strip(), status.strip()
        assert status in {'retain','improve','replace'}
        assert (kind,key) not in actual
        actual.add((kind,key))
        if status == 'replace':
            assert reason.strip().split()[-1] in libraries['professional-icon']
    assert actual == {(kind,key) for kind, lib in libraries.items() for key in lib}
    cfg = yaml.safe_load((ROOT/'gpt-project.yaml').read_text())
    assert 'knowledge/figures/visual-selection-guide.md' in cfg['skills']['definitions'][0]['references']
