import sys,yaml
from pathlib import Path
from pptx import Presentation
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts/itpc'))
from svg_native import draw_svg
from pptx.oxml.ns import qn

def test_original_icons(tmp_path):
 m=yaml.safe_load((ROOT/'knowledge/figures/professional-icons.yaml').read_text());r=Presentation();s=r.slides.add_slide(r.slide_layouts[6])
 assert len(m['icons'])==73
 for k,v in m['icons'].items():draw_svg(s.shapes,v['svg'],0,0,1,1,'247D80')
 draw_svg(s.shapes,'<svg viewBox="0 0 24 24"><path d="M1 1 Q12 20 23 1 Z"/></svg>',0,0,1,1,'247D80')
 out=tmp_path/'test.pptx';r.save(out);s=Presentation(out).slides[0]
 assert len(s.shapes)==74
 assert len(list(s._element.iter(qn('a:cubicBezTo'))))>0
 assert len(list(s._element.iter(qn('a:quadBezTo'))))>0
 assert not list(s._element.iter(qn('p:pic')))
