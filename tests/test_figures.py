import sys
from pathlib import Path
import pytest
import yaml
from pptx import Presentation
from pptx.oxml.ns import qn
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'examples'))
from generate_catalog import generate
from render import render
def test_catalog(tmp_path):
    out=tmp_path/'catalog.pptx'
    generate(out)
    r=Presentation(out)
    icons=yaml.safe_load((ROOT/'knowledge/figures/professional-icons.yaml').read_text())['icons']
    assert len(icons)==127
    assert len(r.slides)==9
    assert {sh.name for slide in r.slides for sh in slide.shapes if sh.name in icons}==set(icons)
    assert all(not list(slide._element.iter(qn('p:pic'))) for slide in r.slides)
def test_retired_figure(tmp_path):
    with pytest.raises(ValueError,match='Unknown object type figure'):
        render({'slides':[{'objects':[dict(type='figure',figure='legacy',x=1,y=1,w=1,h=1)]}]},tmp_path/'old.pptx')
