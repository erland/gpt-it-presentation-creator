import sys,yaml
from pathlib import Path
from pptx import Presentation
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts/itpc'))
from svg_native import draw_svg
from pptx.oxml.ns import qn

def test_original_icons(tmp_path):
 m=yaml.safe_load((ROOT/'knowledge/figures/professional-icons.yaml').read_text());r=Presentation();s=r.slides.add_slide(r.slide_layouts[6])
 # Preserve the original catalog, while allowing deliberate extensions.
 original_ids = ["phosphor/bold/chart-bar","phosphor/bold/check-circle","phosphor/bold/cloud","phosphor/bold/cube","phosphor/bold/database","phosphor/bold/desktop","phosphor/bold/gear","phosphor/bold/hard-drives","phosphor/bold/network","phosphor/bold/robot","phosphor/bold/shield-check","phosphor/bold/sparkle","phosphor/bold/stack","phosphor/bold/user","phosphor/bold/users","phosphor/bold/warning","phosphor/fill/chart-bar","phosphor/fill/check-circle","phosphor/fill/cloud","phosphor/fill/cube","phosphor/fill/database","phosphor/fill/desktop","phosphor/fill/gear","phosphor/fill/hard-drives","phosphor/fill/network","phosphor/fill/robot","phosphor/fill/shield-check","phosphor/fill/sparkle","phosphor/fill/stack","phosphor/fill/user","phosphor/fill/users","phosphor/fill/warning","phosphor/regular/chart-bar","phosphor/regular/check-circle","phosphor/regular/cloud","phosphor/regular/cube","phosphor/regular/database","phosphor/regular/desktop","phosphor/regular/gear","phosphor/regular/hard-drives","phosphor/regular/network","phosphor/regular/robot","phosphor/regular/shield-check","phosphor/regular/sparkle","phosphor/regular/stack","phosphor/regular/user","phosphor/regular/users","phosphor/regular/warning","tabler/filled/alert-triangle","tabler/filled/circle-check","tabler/filled/cloud","tabler/filled/database","tabler/filled/device-desktop","tabler/filled/settings","tabler/filled/shield-check","tabler/filled/sparkles","tabler/filled/user","tabler/outline/alert-triangle","tabler/outline/box","tabler/outline/chart-bar","tabler/outline/circle-check","tabler/outline/cloud","tabler/outline/database","tabler/outline/device-desktop","tabler/outline/layers-intersect","tabler/outline/network","tabler/outline/robot","tabler/outline/server","tabler/outline/settings","tabler/outline/shield-check","tabler/outline/sparkles","tabler/outline/user","tabler/outline/users"]
 assert set(original_ids) <= set(m['icons'])
 for k,v in m['icons'].items():draw_svg(s.shapes,v['svg'],0,0,1,1,'247D80')
 draw_svg(s.shapes,'<svg viewBox="0 0 24 24"><path d="M1 1 Q12 20 23 1 Z"/></svg>',0,0,1,1,'247D80')
 out=tmp_path/'test.pptx';r.save(out);s=Presentation(out).slides[0]
 assert len(s.shapes)==len(m['icons'])+1
 assert len(list(s._element.iter(qn('a:cubicBezTo'))))>0
 assert len(list(s._element.iter(qn('a:quadBezTo'))))>0
 assert not list(s._element.iter(qn('p:pic')))
