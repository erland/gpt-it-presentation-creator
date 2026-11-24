from pathlib import Path
import yaml
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN
ROOT=Path(__file__).resolve().parents[1]
LIB=yaml.safe_load((ROOT/'knowledge/figures/library.yaml').read_text())['figures']
THEMES=yaml.safe_load((ROOT/'knowledge/design/themes.yaml').read_text())['themes']
KINDS=dict(rect=MSO_SHAPE.RECTANGLE,round=MSO_SHAPE.ROUNDED_RECTANGLE,oval=MSO_SHAPE.OVAL,can=MSO_SHAPE.CAN,cloud=MSO_SHAPE.CLOUD,hex=MSO_SHAPE.HEXAGON,pentagon=MSO_SHAPE.PENTAGON,callout=MSO_SHAPE.ROUNDED_RECTANGULAR_CALLOUT,gear=MSO_SHAPE.GEAR_6,fold=MSO_SHAPE.FOLDED_CORNER,trapezoid=MSO_SHAPE.TRAPEZOID,arrow=MSO_SHAPE.RIGHT_ARROW)
def rgb(v):return RGBColor.from_string(v)
def draw(shapes,id,x,y,w,h,t):
    f=LIB[id]
    for kind,a,b,c,d,role in f['parts']:
        xx,yy,ww,hh=x+a*w/100,y+b*h/100,c*w/100,d*h/100
        if kind=='line':
            s=shapes.add_connector(MSO_CONNECTOR.STRAIGHT,*map(Inches,(xx,yy,xx+ww,yy+hh)));s.line.color.rgb=rgb(t[role]);s.line.width=Pt(2)
        else:
            s=shapes.add_shape(KINDS[kind],*map(Inches,(xx,yy,ww,hh)));s.fill.solid();s.fill.fore_color.rgb=rgb(t[role]);s.line.fill.background()
            if kind=='round':s.adjustments[0]=.12
        style=s._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
        if style is not None:s._element.remove(style)
    for child,a,b,c,d in f.get('components',[]):draw(shapes,child,x+a*w/100,y+b*h/100,c*w/100,d*h/100,t)
def text(s,x,y,w,h,v,t,size,bold=False,center=False):
    a=s.shapes.add_textbox(*map(Inches,(x,y,w,h)));f=a.text_frame;f.clear();f.word_wrap=True;f.margin_left=f.margin_right=f.margin_top=f.margin_bottom=0;p=f.paragraphs[0];p.text=v;p.font.name='Aptos';p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=rgb(t);p.alignment=PP_ALIGN.CENTER if center else PP_ALIGN.LEFT

def generate(path):
    r=Presentation();r.slide_width=Inches(13.333);r.slide_height=Inches(7.5)
    cats=list(dict.fromkeys(f['category'] for f in LIB.values()))
    for theme,t in THEMES.items():
        for cat in cats:
            ids=[id for id,f in LIB.items() if f['category']==cat];s=r.slides.add_slide(r.slide_layouts[6]);s.background.fill.solid();s.background.fill.fore_color.rgb=rgb(t['background']);text(s,.65,.35,12,.3,'FIGURBIBLIOTEK  /  '+theme.upper().replace('-',' '),t['muted'],12,True);text(s,.65,.85,12,.7,cat,t['text'],34,True)
            cols=5 if len(ids)>6 else (3 if len(ids)>4 else 4);rows=(len(ids)+cols-1)//cols;cw=12/cols;ch=4.8/rows
            for i,id in enumerate(ids):
                x=.65+(i%cols)*cw;y=1.8+(i//cols)*ch;size=min(cw-.35,ch-.72,2.65);g=s.shapes.add_group_shape();g.name=id;draw(g.shapes,id,x+(cw-size)/2,y+.1,size,size,t);text(s,x+.05,y+size+.2,cw-.1,.6,LIB[id]['label'],t['text'],15,True,True)
            text(s,.65,7.02,12,.3,'IT PRESENTATION CREATOR   /   Redigerbara, grupperade PowerPoint-former',t['muted'],11)
    r.save(path)
if __name__=='__main__':generate(ROOT/'examples/figure-catalog.pptx')
