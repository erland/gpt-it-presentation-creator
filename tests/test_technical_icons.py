from pathlib import Path
import hashlib
import sys
import yaml
from pptx import Presentation
from pptx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/itpc'))
from svg_native import draw_svg

def test_technical_icons(tmp_path):
    library = yaml.safe_load((ROOT/'knowledge/figures/professional-icons.yaml').read_text())
    register = yaml.safe_load((ROOT/'knowledge/figures/technical-icon-register.yaml').read_text())
    icons = library['icons']
    assert len(register['concepts']) == 63
    new = {k:v for k,v in icons.items() if 'source_blob_sha' in v}
    assert len(new) == 54
    for key, item in new.items():
        data = item['svg'].encode()
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == item['source_blob_sha'], key
    for item in register['concepts'].values():
        assert item['preferred_icon'] in icons
    p = Presentation()
    for key in sorted(set(x['preferred_icon'] for x in register['concepts'].values())):
        s = p.slides.add_slide(p.slide_layouts[6])
        draw_svg(s.shapes, icons[key]['svg'], 1,1,1,1,'205C63')
        assert list(s._element.iter(qn('a:custGeom'))), key
        assert not list(s._element.iter(qn('p:pic'))), key
    out = tmp_path/'technical-icons.pptx'
    p.save(out)
    assert len(Presentation(out).slides) == len(register['concepts'])
