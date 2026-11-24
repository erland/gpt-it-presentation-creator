from pathlib import Path
import sys,yaml
from pptx import Presentation
from pptx.oxml.ns import qn
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'examples'))
from compose_generations import build,render

def test_composition(tmp_path):
    model=build(); assert len(model['slides'])==5
    assert len(model['slides'][0]['objects'])==4
    out=tmp_path/'composed.pptx';render(model,out)
    r=Presentation(out);assert len(r.slides)==5
    for s in r.slides:
        assert not list(s._element.iter(qn('p:pic')))
        assert list(s._element.iter(qn('a:t')))
    assert len(list(r.slides[0]._element.iter(qn('a:headEnd'))))>0

def test_gate_in_all_skills():
    config=yaml.safe_load((ROOT/'gpt-project.yaml').read_text())
    for skill in config['skills']['definitions']:
        assert 'knowledge/visual-acceptance.md' in skill['references']
        assert 'Obligatorisk visuell acceptansgrind' in (ROOT/skill['source']).read_text()
