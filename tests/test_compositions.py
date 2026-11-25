import sys
from pathlib import Path
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts/itpc'));sys.path.insert(0,str(ROOT/'examples'))
from generations import build
from render import render,transform_objects

def test_compositions(tmp_path):
    m=build();p=tmp_path/'test.pptx';render(m,p);r=Presentation(p)
    assert len(r.slides)==5 and len(r.slides[0].shapes)==4
    for i in range(4):
        a=r.slides[0].shapes[i];b=r.slides[i+1].shapes[0]
        assert len(a.shapes)==len(b.shapes)
        assert b.width>a.width
        assert 'headEnd' in b._element.xml and 'tailEnd' in b._element.xml
    assert 'custGeom' in r.slides[0]._element.xml
    assert transform_objects([{'type':'line','from':[1,2],'to':[3,4],'stroke_pt':1}],2,1,1)[0]['to']==[7,9]
