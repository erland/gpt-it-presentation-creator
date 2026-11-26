"""Regression gate for complex, freely composed reference presentations."""
import shutil
import sys
from pathlib import Path

import pytest
from pptx import Presentation
from pptx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'examples'))
from advanced_compositions import build_model, produce
from quality import audit

HEADLINES=(
    'Från driftbeställningar till verksamhetsdriven utveckling',
    'Från fristående AI-tjänster till intelligenta arbetsflöden',
    'En gemensam datagrund breddar analysmöjligheterna',
)

def test_complex_cases_have_distinct_layouts_and_valid_assets(tmp_path):
    model=build_model()
    assert len(model['slides'])==3
    assert model['size']==[13.333,7.5]
    counts=[]
    icons=set()
    for slide,headline in zip(model['slides'],HEADLINES):
        objects=slide['objects']
        assert any(o.get('text')==headline for o in objects)
        assert all(o['type'] in {'text','shape','line','professional-icon','path','group'} for o in objects)
        assert any(o['type']=='line' for o in objects)
        assert sum(o['type']=='professional-icon' for o in objects)>=5
        assert sum(o['type']=='shape' for o in objects)>=10
        assert sum(o['type']=='text' for o in objects)>=15
        counts.append(len(objects))
        icons.update(o['icon'] for o in objects if o['type']=='professional-icon')
    assert all(n>=50 for n in counts),counts
    assert len(set(counts))>1
    assert all(i.startswith('phosphor/regular/') for i in icons)

def test_background_aware_quality_accepts_verified_dark_header_bands():
    model=build_model()
    assert not audit(model), 'Real invalid contrast or text-fit errors must remain visible'

def test_editable_powerpoint_has_no_rasters(tmp_path):
    review=produce(tmp_path,preview=False)
    assert not review['unresolved_audit_warnings']
    assert len(review['slides'])==3
    assert all(x['raster_pictures']==0 for x in review['slides'])
    assert min(x['editable_vector_shapes'] for x in review['slides'])>=8
    assert min(x['shapes'] for x in review['slides'])>=50
    prs=Presentation(tmp_path/'advanced-compositions.pptx')
    assert all(not list(s._element.iter(qn('p:pic'))) for s in prs.slides)

def test_actual_png_previews(tmp_path):
    if not shutil.which('libreoffice') or not shutil.which('pdftoppm'):
        pytest.skip('Requires LibreOffice and Poppler')
    report=produce(tmp_path,preview=True)
    assert len(report['previews'])==3
    assert all((tmp_path/p).stat().st_size>10_000 for p in report['previews'])
    assert (tmp_path/'contact-sheet.png').stat().st_size>30_000
    assert len(report['rendered_text_placement'])==3
    assert all(row['heading_line_delta_pt']<=6 for row in report['rendered_text_placement'])
