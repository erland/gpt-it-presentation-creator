import sys
from pathlib import Path
import pytest
import yaml
from pptx import Presentation
from pptx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/itpc'))
from render import render, transform_objects

def test_zone_and_flow_editable(tmp_path):
    m=yaml.safe_load((ROOT/'examples/graphic-blocks.yaml').read_text())
    out=tmp_path/'blocks.pptx'
    render(m,out)
    p=Presentation(out)
    assert len(p.slides)==1
    slide=p.slides[0]
    assert not list(slide._element.iter(qn('p:pic')))
    assert len(list(slide._element.iter(qn('a:prstDash'))))>=3
    assert len(list(slide._element.iter(qn('a:alpha'))))==2
    assert any(s.name == 'Group 1' or s.shape_type == 6 for s in slide.shapes)
    assert any(s.has_text_frame and 'Molnplattform' in s.text for s in slide.shapes)

@pytest.mark.parametrize('obj',[
 {'type':'line','from':[1,1],'to':[2,2],'stroke_dash':'invalid'},
 {'type':'shape','x':1,'y':1,'w':2,'h':2,'fill_opacity':-0.1},
 {'type':'shape','x':1,'y':1,'w':2,'h':2,'fill_opacity':1.01},
 {'type':'shape','x':1,'y':1,'w':2,'h':2,'fill':'none','fill_opacity':0.5},
 {'type':'shape','x':1,'y':1,'w':2,'h':2,'stroke_dash':'dash'},
 {'type':'shape','x':1,'y':1,'w':2,'h':2,'fill_opacity':0.5,'gradient':['primary','accent']},
])
def test_invalid_styles_rejected(tmp_path,obj):
    with pytest.raises(ValueError):
        render({'slides':[{'objects':[obj]}]},tmp_path/'invalid.pptx')

def test_transforms_preserve_styles():
    o=[{'type':'shape','x':1,'y':1,'w':2,'h':1,'stroke':'accent','stroke_pt':2,'stroke_dash':'dash','fill_opacity':.4}]
    scaled=transform_objects(o,2,1,1)
    assert scaled[0]['x']==3 and scaled[0]['stroke_pt']==4
    assert scaled[0]['stroke_dash']=='dash' and scaled[0]['fill_opacity']==.4
    assert o[0]['x']==1
