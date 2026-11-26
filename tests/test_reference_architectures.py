from pathlib import Path
import sys
import shutil

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'examples'))
sys.path.insert(0,str(ROOT/'scripts/itpc'))
from render_reference_architectures import load_model,create
from quality import audit

HEADINGS=(
    'En gemensam leveransmodell för flera driftsmiljöer',
    'Händelser minskar direkta beroenden mellan IT-stöd',
    'En delad datagrund för flera analysbehov',
    'AI-assistenter samverkar med kunskap och IT-stöd',
)

def test_reference_model_and_editable_objects(tmp_path):
    m=load_model()
    assert m['size']==[13.333,7.5]
    assert len(m['slides'])==4
    assert not audit(m)
    icons=[]
    for slide,heading in zip(m['slides'],HEADINGS):
        objects=slide['objects']
        assert any(obj.get('text')==heading for obj in objects)
        assert all(obj['type'] not in {'figure','icon','image'} for obj in objects)
        assert sum(obj['type']=='professional-icon' for obj in objects)>=3
        assert sum(obj['type']=='shape' for obj in objects)>=8
        icons.extend(obj['icon'] for obj in objects if obj['type']=='professional-icon')
    assert all(name.startswith('phosphor/regular/') for name in icons)
    report=create(tmp_path)
    assert len(report['slides'])==4
    assert sum(item['raster_pictures'] for item in report['slides'])==0
    assert all(item['editable_custom_geometries']>=3 for item in report['slides'])
    assert report['slides'][1]['dashed_elements']==4
    assert (tmp_path/'reference-architectures.pptx').exists()

def test_real_powerpoint_previews(tmp_path):
    if not shutil.which('libreoffice') or not shutil.which('pdftoppm'):
        import pytest
        pytest.skip('Actual previews require LibreOffice and Poppler')
    report=create(tmp_path,with_previews=True)
    assert len(report['rendered_previews'])==4
    assert all((tmp_path/p).stat().st_size>5000 for p in report['rendered_previews'])
    assert (tmp_path/'contact-sheet.png').stat().st_size>10000
