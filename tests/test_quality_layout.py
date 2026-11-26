"""DEV-012F: visual quality and semantic connector regression tests."""
import sys
from pathlib import Path

import pytest
from pptx import Presentation
from pptx.util import Inches

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/itpc'))
from quality import audit,correct,contrast,estimate_text_lines,suggest_text_size
from render import render,resolve_anchored_lines,transform_objects

def model(objects):
    return {'theme':'executive-clean','slides':[{'objects':objects}]}

def panel(x=1,y=1,w=3,h=1,fill='183B56',opacity=None):
    p={'type':'shape','id':'panel','x':x,'y':y,'w':w,'h':h,
       'fill':fill,'allow_overlap':True}
    if opacity is not None:p['fill_opacity']=opacity
    return p

def label(color='FFFFFF',x=1.2,y=1.3,w=2.4,h=.45,value='Platform'):
    return {'type':'text','x':x,'y':y,'w':w,'h':h,
            'text':value,'size':20,'bold':True,'color':color}

def test_opaque_overlaid_text_uses_real_contrast():
    good=model([panel(),label()])
    assert not [i for i in audit(good) if i['code'] in ('contrast','contrast_unknown')]
    assert correct(good)==good
    bad=model([panel(),label(color='000000')])
    assert any(i['code']=='contrast' for i in audit(bad))
    fixed=correct(bad)
    assert fixed['slides'][0]['objects'][1]['color']=='FFFFFF'
    assert not [i for i in audit(fixed) if i['code']=='contrast']

def test_translucency_is_composited_in_z_order():
    objects=[panel(fill='000000'),panel(fill='FFFFFF',opacity=.70),
             label(color='000000',value='Readable')]
    # Duplicate IDs are not involved in contrast model checks.
    assert not [i for i in audit(model(objects)) if i['code'] in ('contrast','contrast_unknown')]
    objects[-1]['color']='FFFFFF'
    assert any(i['code']=='contrast' for i in audit(model(objects)))

def test_unknown_partial_and_gradient_background_is_not_assumed_safe():
    p=panel(w=1.4)
    assert any(i['code']=='contrast_unknown' for i in audit(model([p,label()])))
    g=panel();g['gradient']=['primary','secondary']
    assert any(i['code']=='contrast_unknown' for i in audit(model([g,label()])))

def test_word_aware_text_estimate_handles_spaces_and_explicit_breaks():
    assert estimate_text_lines('a\nb',200,18)==2
    assert estimate_text_lines('aaa bbb ccc',60,14)>=2
    assert estimate_text_lines('Supercalifragilisticexpialidocious',60,14)>=3
    assert estimate_text_lines('',160,18)==1

def test_anchored_connectors_follow_actual_component_edges(tmp_path):
    objects=[
        {'type':'shape','id':'source','x':1,'y':1,'w':2,'h':1},
        {'type':'shape','id':'target','x':6,'y':2,'w':2,'h':1},
        {'type':'line','from_id':'source','to_id':'target',
         'from_side':'right','to_side':'left','arrow':True}
    ]
    before=str(objects)
    resolved=resolve_anchored_lines(objects)
    assert resolved[2]['from']==[3,1.5]
    assert resolved[2]['to']==[6,2.5]
    assert str(objects)==before
    pptx=tmp_path/'anchors.pptx'
    render(model(objects),pptx)
    prs=Presentation(pptx);connector=prs.slides[0].shapes[2]
    assert connector.begin_x==Inches(3) and connector.begin_y==Inches(1.5)
    assert connector.end_x==Inches(6) and connector.end_y==Inches(2.5)

def test_anchor_works_in_groups_and_reusable_transforms():
    objects=[{'type':'group','children':[{'type':'shape','id':'a','x':1,'y':1,'w':1,'h':2}]},
             {'type':'shape','id':'b','x':4,'y':3,'w':2,'h':1},
             {'type':'line','from_id':'a','to_id':'b','from_side':'bottom','to_side':'top'}]
    scaled=transform_objects(objects,1.5,1,.5)
    result=resolve_anchored_lines(scaled)
    assert result[2]['from']==[3.25,5]
    assert result[2]['to']==[8.5,5]

@pytest.mark.parametrize('line,fragment',[
    ({'type':'line','from_id':'a','to_id':'missing'},'Unknown connection anchor'),
    ({'type':'line','from_id':'a'},'requires both'),
    ({'type':'line','from_id':'a','to_id':'b','from_side':'diagonal'},'Unknown anchor side'),
    ({'type':'line','from_id':'a','to_id':'b','from':[1,1]},'cannot also specify'),
])
def test_invalid_semantic_connectors_rejected(line,fragment):
    objects=[{'type':'shape','id':'a','x':1,'y':1,'w':2,'h':1},
             {'type':'shape','id':'b','x':4,'y':1,'w':2,'h':1},line]
    with pytest.raises(ValueError,match=fragment):
        resolve_anchored_lines(objects)

def test_duplicate_anchor_id_is_rejected():
    with pytest.raises(ValueError,match='Duplicate anchor id'):
        resolve_anchored_lines([
            {'type':'shape','id':'same','x':1,'y':1,'w':1,'h':1},
            {'type':'shape','id':'same','x':3,'y':1,'w':1,'h':1}])

def test_suggest_text_size_never_drops_below_legibility_floor():
    assert suggest_text_size('Short title',4,1,preferred_pt=26)>=14
    assert suggest_text_size('Short title',4,1,preferred_pt=26)<=26
    with pytest.raises(ValueError,match='No legible text size'):
        suggest_text_size('Too many technical words to fit in a tiny box',.3,.12)
    with pytest.raises(ValueError,match='Invalid text-fit'):
        suggest_text_size('Bad floor',2,1,min_pt=11)

def test_anchored_architecture_example_renders_in_source_order(tmp_path):
    import yaml
    from pptx.oxml.ns import qn
    source=yaml.safe_load((ROOT/'examples/anchored-connections.yaml').read_text())
    # Connections intentionally occur before component declarations.
    assert source['slides'][0]['objects'][2]['from_id']=='service'
    resolved=resolve_anchored_lines(source['slides'][0]['objects'])
    assert resolved[2]['from']==[3.6,3.4]
    assert resolved[2]['to']==[5.45,3.4]
    assert resolved[3]['from']==[6.825,4.2]
    assert resolved[3]['to']==[6.825,5.05]
    assert not [x for x in audit(source) if x['code'] in {'contrast','contrast_unknown','small_text'}]
    pptx=tmp_path/'anchored.pptx'
    render(source,pptx)
    prs=Presentation(pptx)
    assert len(prs.slides)==1
    assert not list(prs.slides[0]._element.iter(qn('p:pic')))
    connectors=[x for x in prs.slides[0].shapes if x.shape_type==9]
    assert len(connectors)==2
