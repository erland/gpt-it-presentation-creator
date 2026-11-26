from pathlib import Path
import sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts/itpc'));sys.path.insert(0,str(R/'examples/acceptance'))
from generate import decks
from render import render
from quality import audit
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

def test_acceptance(tmp_path):
 for name,model in decks():
  assert not audit(model)
  p=tmp_path/(name+'.pptx');render(model,p);r=Presentation(p)
  assert len(r.slides)==2
  for s in r.slides:
   assert any(x.shape_type==MSO_SHAPE_TYPE.GROUP for x in s.shapes)
   assert all(x.shape_type!=MSO_SHAPE_TYPE.PICTURE for x in s.shapes)
   assert all(x.left>=0 and x.top>=0 and x.left+x.width<=r.slide_width and x.top+x.height<=r.slide_height for x in s.shapes)

def test_checked_in_acceptance_examples_render(tmp_path):
 import yaml
 from pptx.oxml.ns import qn
 for name in ('ai','generationer','plattform'):
  model=yaml.safe_load((R/'examples/acceptance'/f'{name}.yaml').read_text())
  assert not audit(model), name
  out=tmp_path/f'{name}-checked-in.pptx'
  render(model,out)
  p=Presentation(out)
  assert len(p.slides)==2
  assert any(sh.shape_type==MSO_SHAPE_TYPE.GROUP for slide in p.slides for sh in slide.shapes)
  assert all(not list(slide._element.iter(qn('p:pic'))) for slide in p.slides)
