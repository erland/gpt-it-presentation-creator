import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'examples'))
from generate_catalog import LIB,THEMES,KINDS,ROOT
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

def test_library():
    assert len(LIB)==30
    def check(id,seen):
        assert id not in seen
        f=LIB[id]
        for kind,x,y,w,h,role in f['parts']:
            assert kind=='line' or kind in KINDS
            assert all(0<=v<=100 for v in (x,y,x+w,y+h))
            assert all(role in t for t in THEMES.values())
        for child,x,y,w,h in f.get('components',[]):
            assert w>0 and h>0 and 0<=x<=x+w<=100 and 0<=y<=y+h<=100
            check(child,seen|{id})
    for id in LIB:check(id,set())
def test_catalog():
    r=Presentation(ROOT/'examples/figure-catalog.pptx');assert len(r.slides)==15
    groups=[]
    for s in r.slides:
        for sh in s.shapes:
            assert sh.left>=0 and sh.top>=0 and sh.left+sh.width<=r.slide_width and sh.top+sh.height<=r.slide_height
            if sh.shape_type==MSO_SHAPE_TYPE.GROUP:
                groups.append(sh.name);assert len(sh.shapes)>0
                assert all(x.shape_type!=MSO_SHAPE_TYPE.PICTURE for x in sh.shapes)
    assert sorted(groups)==sorted(list(LIB)*3)
