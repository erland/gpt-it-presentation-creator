from pathlib import Path
from tempfile import TemporaryDirectory
from render import render
from pptx import Presentation
import yaml
from pptx.enum.shapes import MSO_SHAPE_TYPE
p=Path(__file__).parent
with TemporaryDirectory() as d:
    out=Path(d)/'demo.pptx'; model=yaml.safe_load((p/'demo.yaml').read_text());render(model,out,p);r=Presentation(out)
    assert len(r.slides)==2
    assert sum(s.shape_type==MSO_SHAPE_TYPE.GROUP for slide in r.slides for s in slide.shapes)==3
    assert any(s.has_text_frame and 'självservice' in s.text for s in r.slides[0].shapes)
    try:render({'slides':[{'objects':[{'type':'text','x':99,'y':0,'w':1,'h':1}]}]},out)
    except ValueError:pass
    else:raise AssertionError('Bounds validation failed')
print('PASS: deck generation, editable groups and text, invalid bounds rejection')
