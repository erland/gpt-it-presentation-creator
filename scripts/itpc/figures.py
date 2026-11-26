from pathlib import Path
import yaml
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN
ROOT=Path(__file__).resolve().parents[2]
THEMES=yaml.safe_load((ROOT/'knowledge/design/themes.yaml').read_text())['themes']
KINDS=dict(rect=MSO_SHAPE.RECTANGLE,round=MSO_SHAPE.ROUNDED_RECTANGLE,oval=MSO_SHAPE.OVAL,can=MSO_SHAPE.CAN,cloud=MSO_SHAPE.CLOUD,hex=MSO_SHAPE.HEXAGON,pentagon=MSO_SHAPE.PENTAGON,callout=MSO_SHAPE.ROUNDED_RECTANGULAR_CALLOUT,gear=MSO_SHAPE.GEAR_6,fold=MSO_SHAPE.FOLDED_CORNER,trapezoid=MSO_SHAPE.TRAPEZOID,arrow=MSO_SHAPE.RIGHT_ARROW)
def rgb(v):return v if isinstance(v,RGBColor) else RGBColor.from_string(v)
