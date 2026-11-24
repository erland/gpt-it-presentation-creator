import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/itpc'))
from quality import audit,correct,contrast

def test_quality():
    m={'slides':[{'objects':[{'type':'text','x':1,'y':1,'w':3,'h':1,'text':'Test','color':'FFFFFF','size':20}]}]}
    assert any(i['code']=='contrast' for i in audit(m))
    assert not audit(correct(m));assert m['slides'][0]['objects'][0]['color']=='FFFFFF'
    assert contrast('000000','FFFFFF')==21

def test_overlap():
    o={'type':'shape','x':1,'y':1,'w':2,'h':2};m={'slides':[{'objects':[o,dict(o)]}]}
    assert any(i['code']=='overlap' for i in audit(m));m['slides'][0]['objects'][1]['allow_overlap']=True;assert not audit(m)
