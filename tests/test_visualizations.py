from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'examples'))
from generate_visualizations import P, ICONS, THEMES, ROOT, generate
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

def test_patterns():
 assert len(P)==10
 assert len({p['family'] for p in P.values()})==5
 assert all(sum(q['family']==p['family'] for q in P.values())==2 for p in P.values())
 assert all(set(p['icons'])<=set(ICONS) for p in P.values())

def test_catalog(tmp_path):
 out=tmp_path/'visualization-catalog.pptx'
 generate(out)
 r=Presentation(out)
 assert len(r.slides)==len(P)*len(THEMES)
 for s in r.slides:
  assert any(a.shape_type==MSO_SHAPE_TYPE.GROUP for a in s.shapes)
  assert not any(a.shape_type==MSO_SHAPE_TYPE.PICTURE for a in s.shapes)
  for a in s.shapes:
   assert a.left>=0 and a.top>=0 and a.left+a.width<=r.slide_width and a.top+a.height<=r.slide_height, a.name
