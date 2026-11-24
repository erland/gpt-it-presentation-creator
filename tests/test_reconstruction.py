from pathlib import Path
import sys,yaml
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts/itpc'))
from render import render, ICONS

def test_reconstruction(tmp_path):
 m=yaml.safe_load((R/'examples/reconstruction.yaml').read_text());p=tmp_path/'r.pptx';render(m,p);r=Presentation(p);s=r.slides[0];assert len(ICONS)>=20
 assert not any(x.shape_type==MSO_SHAPE_TYPE.PICTURE for x in s.shapes)
 assert sum(x.shape_type==MSO_SHAPE_TYPE.GROUP for x in s.shapes)>=20
 assert 'Förflyttning till verksamhetsintegrerad AI' in [x.text for x in s.shapes if x.has_text_frame]
 assert 'gradFill' in s._element.xml and 'custGeom' in s._element.xml
