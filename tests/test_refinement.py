import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Pt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/itpc'))
from render import render, transform_objects

def test_filled_and_scaled(tmp_path):
    o=dict(type='icon',icon='check-filled',x=1,y=1,w=1,h=1,color='65963E')
    p=tmp_path/'test.pptx';render({'slides':[{'objects':[o]},{'objects':transform_objects([o],2)}]},p)
    r=Presentation(p);a,b=[s.shapes[0].shapes for s in r.slides]
    assert str(a[0].fill.fore_color.rgb)=='65963E'
    assert b[1].line.width==2*a[1].line.width
