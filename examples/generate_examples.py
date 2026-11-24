from pathlib import Path
import yaml
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR
p=Path(__file__).resolve().parents[1]; themes={
'executive-clean':dict(background='F5F7FA',text='183B56',muted='486477',surface='FFFFFF',primary='183B56',accent='2878AD',secondary='70B8BC',line='DCE6EF',on_primary='FFFFFF'),
'modern-technology':dict(background='142038',text='FFFFFF',muted='B9C9E1',surface='24334D',primary='345B9E',accent='47B8CE',secondary='9474D8',line='30415D',on_primary='FFFFFF'),
'editorial-professional':dict(background='F7F5EF',text='344C47',muted='52665D',surface='FFFFFF',primary='344C47',accent='B98C42',secondary='77968B',line='DEDACD',on_primary='FFFFFF')}
(p/'knowledge/design/themes.yaml').write_text(yaml.safe_dump({'version':1,'themes':themes,'layout':{'width_in':13.333,'height_in':7.5,'margin_in':0.55,'gap_in':0.24,'title_pt':36,'body_pt':20,'label_pt':15,'font':'Aptos'}},sort_keys=False))
r=Presentation();r.slide_width=Inches(13.333);r.slide_height=Inches(7.5)
def rgb(c):return RGBColor.from_string(c)
def rect(s,x,y,w,h,c,shape=MSO_SHAPE.RECTANGLE):
 a=s.shapes.add_shape(shape,*map(Inches,(x,y,w,h)));a.fill.solid();a.fill.fore_color.rgb=rgb(c);a.line.fill.background();a._element.remove(a._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style'));return a
def txt(s,x,y,w,h,t,c,sz=20,b=False):
 a=s.shapes.add_textbox(*map(Inches,(x,y,w,h)));f=a.text_frame;f.clear();f.word_wrap=True;f.margin_left=f.margin_right=f.margin_top=f.margin_bottom=0; q=f.paragraphs[0];q.text=t;q.font.name='Aptos';q.font.size=Pt(sz);q.font.bold=b;q.font.color.rgb=rgb(c);return a
for i,(name,t) in enumerate(themes.items()):
 s=r.slides.add_slide(r.slide_layouts[6]);s.background.fill.solid();s.background.fill.fore_color.rgb=rgb(t['background']); fg=t['text']; m=t['muted']; ac=t['accent'];
 txt(s,.65,.35,11,.3,'IT PRESENTATION CREATOR  /  '+name.replace('-',' ').upper(),m,12,True)
 txt(s,.65,.85,12,1.0,'Från teknikbeställning till självservice',fg,36,True)
 txt(s,.65,1.75,12,.5,'Samma behov. Ett nytt sätt att leverera IT.',m,20)
 if i==0:
  for x,label,items in [(0.65,'NULÄGE',['Beställ databas','Beställ nätverk','Beställ driftmiljö']),(7.05,'MÅLBILD',['Välj plattformstjänst','Konfigurera själv','Leverera IT-stöd'])]:
   rect(s,x,2.55,5.6,3.65,t['surface']);rect(s,x,2.55,5.6,.09,t['line'] if x<1 else ac);txt(s,x+.3,2.85,5,.4,label,m,15,True)
   for j,item in enumerate(items):
    rect(s,x+.3,3.45+j*.76,.12,.42,t['secondary'] if x<1 else ac);txt(s,x+.58,3.43+j*.76,4.7,.55,item,fg,22,True)
  rect(s,6.38,4.0,.53,.45,ac,MSO_SHAPE.RIGHT_ARROW)
 elif i==1:
  txt(s,.7,2.65,4.1,.5,'FRAGMENTERADE BESTÄLLNINGAR',m,15,True)
  for j,label in enumerate(['Databas','Nätverk','Driftmiljö']):
   rect(s,.7,3.25+j*.78,3.6,.58,t['surface']);txt(s,.9,3.35+j*.78,3.2,.4,label,fg,19)
  rect(s,4.65,4.0,1.0,.65,ac,MSO_SHAPE.RIGHT_ARROW)
  rect(s,6.05,2.65,6.6,3.5,t['surface']);txt(s,6.35,2.95,6,.5,'SJÄLVSERVICEPLATTFORM',ac,17,True)
  for j,label in enumerate(['Välj','Konfigurera','Leverera']):
   x=6.35+j*2.03;rect(s,x,3.65,1.85,1.4,t['primary']);txt(s,x+.13,4.12,1.65,.5,label,'FFFFFF',18,True)
  rect(s,6.35,5.35,5.91,.15,ac);txt(s,6.35,5.58,5.9,.35,'Gemensamma plattformstjänster',m,15)
 else:
  txt(s,.7,2.65,4.5,.45,'01 / Beställning',m,17,True);txt(s,.7,3.25,4.6,1.4,'IT levererar\nkomponenter',fg,31,True);txt(s,.7,4.85,4.5,1.0,'Databas, nätverk och driftmiljö beställs var för sig.',m,20)
  rect(s,5.45,2.65,.04,3.5,t['line']);rect(s,5.72,4.0,.7,.4,ac,MSO_SHAPE.RIGHT_ARROW)
  txt(s,6.8,2.65,5.5,.45,'02 / Självservice',m,17,True);txt(s,6.8,3.25,5.5,1.4,'IT möjliggör\nleverans',fg,31,True);txt(s,6.8,4.85,5.5,1.0,'Team väljer och konfigurerar gemensamma plattformstjänster.',m,20)
 rect(s,.65,6.55,12.03,.025,t['line']);txt(s,.65,6.78,11.6,.4,'Förflyttningen: från separata beställningar till sammanhållen leverans.',fg,16,True);txt(s,12.15,6.78,.5,.4,str(i+1),m,14)
r.save(p/'examples/design-styles.pptx')
# contrast and structural tests
