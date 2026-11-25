import sys
from pathlib import Path
from pptx import Presentation
from pptx.oxml.ns import qn
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/itpc'))
from render import render, transform_objects

def test_filled_and_scaled(tmp_path):
    o=dict(type='professional-icon',icon='phosphor/fill/check-circle',x=1,y=1,w=1,h=1,color='65963E')
    p=tmp_path/'test.pptx';render({'slides':[{'objects':[o]},{'objects':transform_objects([o],2)}]},p)
    r=Presentation(p);a,b=[s.shapes[0].shapes for s in r.slides]
    assert str(a[0].fill.fore_color.rgb)=='65963E'
    assert b[0].width == 2*a[0].width
    assert b[0].height == 2*a[0].height
    assert str(b[0].fill.fore_color.rgb)=='65963E'
    for slide in r.slides:
        assert list(slide._element.iter(qn('a:custGeom')))
        assert not list(slide._element.iter(qn('p:pic')))

def test_retired_icon_type_rejected(tmp_path):
    o=dict(type='icon',icon='check-filled',x=1,y=1,w=1,h=1)
    with pytest.raises(ValueError, match='Unknown object type icon'):
        render({'slides':[{'objects':[o]}]},tmp_path/'retired.pptx')
