from generate_catalog import *
from pptx.enum.shapes import MSO_SHAPE
P=yaml.safe_load((ROOT/'knowledge/visualizations/patterns.yaml').read_text())['patterns']
def generate(path):
 r=Presentation();r.slide_width=Inches(13.333);r.slide_height=Inches(7.5)
 for theme,t in THEMES.items():
  for key,p in P.items():
   s=r.slides.add_slide(r.slide_layouts[6]);s.background.fill.solid();s.background.fill.fore_color.rgb=rgb(t['background'])
   def txt(x,y,w,h,v,size=18,b=False,c=False):text(s,x,y,w,h,v,t['text'],size,b,c)
   def fig(id,x,y,w,h):
    g=s.shapes.add_group_shape();g.name=id;draw(g.shapes,id,x,y,w,h,t)
   def panel(x,y,w,h,role='surface'):
    a=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,*map(Inches,(x,y,w,h)));a.fill.solid();a.fill.fore_color.rgb=rgb(t[role]);a.line.fill.background();a.adjustments[0]=.08
    st=a._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style');a._element.remove(st) if st is not None else None
   def arrow(x,y,w=.65):
    a=s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,*map(Inches,(x,y,w,.28)));a.fill.solid();a.fill.fore_color.rgb=rgb(t['accent']);a.line.fill.background()
   def item(id,label,x,y,w=2.5,h=2.5):
    z=min(w-.3,h-.65);fig(id,x+(w-z)/2,y,z,z);txt(x,y+z+.08,w,.65,label,17,True,True)
   titles={'comparison':'Från teknikbeställning till självservice','destination':'Självservice frigör tid för verksamheten','journey':'Fyra generationer av IT-leverans','staircase':'IT blir successivt en möjliggörare','layers':'Gemensamma lager förenklar IT-stöden','foundation':'En plattform möjliggör många IT-stöd','capability-map':'Förmågor formar ett gemensamt erbjudande','capability-hub':'Plattformen samlar återanvändbara förmågor','pipeline':'Information förädlas till analys','branching':'Samma data kan skapa nytta på flera sätt'}
   text(s,.65,.35,12,.3,p['family'].upper()+'  /  '+theme.upper(),t['muted'],11,True);txt(.65,.85,12,1,titles[key],32,True)
   if key=='comparison':
    for x,id,label,desc in [( .65,'legacy','Nuläge','Separata beställningar'),(7.05,'platform','Målbild','Gemensamma tjänster')]:
     panel(x,2,5.6,4.55);txt(x+.3,2.25,5,.5,label,23,True);fig(id,x+1.4,2.9,2.8,2.8);txt(x+.3,5.9,5,.45,desc,19,False,True)
    arrow(6.35,4.1,.55)
   elif key=='destination':
    item('legacy','Teknikbeställning',.8,3.25,3,2.8);arrow(4,4.2,1.2);panel(5.6,1.95,7.05,4.65);fig('platform',6,2.3,3.6,3.6);txt(9.65,3.1,2.7,1.1,'Självservice',25,True);txt(9.65,4.3,2.6,1.3,'Team kan fokusera på verksamhetens behov.',19)
   elif key in ('journey','staircase'):
    for i,(id,label) in enumerate(zip(p['figures'],['Monolit','Komponenter','Plattform','Verksamhetsdriven IT'])):
     x=.7+i*3.1;y=2.6 if key=='journey' else 3.8-i*.55;panel(x,y,2.7,2.8);item(id,label,x+.08,y+.12,2.54,2.5); 
     if i<3 and key=='journey':arrow(x+2.76,y+1.1,.28)
   elif key=='layers':
    for i,(id,label,desc) in enumerate(zip(p['figures'],['IT-stöd','Plattformstjänster','Infrastruktur'],['Verksamhetsnära funktioner','Gemensamma tekniska förmågor','Beräkning, lagring och nätverk'])):
     y=1.95+i*1.53;panel(.75,y,11.8,1.36);fig(id,1,y+.08,1.2,1.2);txt(2.55,y+.23,4,.5,label,22,True);txt(6.3,y+.28,5.8,.8,desc,18)
   elif key=='foundation':
    for i,(id,label) in enumerate(zip(p['figures'][:3],['IT-stöd','AI-assistent','Analys'])):item(id,label,1.1+i*4.1,2,3,2.8)
    panel(.8,5,11.75,1.5);fig('platform',1,5.12,1.25,1.25);txt(2.6,5.3,9.5,.9,'Gemensam plattform • återanvändbara tjänster',24,True)
   elif key=='capability-map':
    for i,(id,label) in enumerate(zip(p['figures'],['Integration','Data','Säkerhet','Automation','Analys','AI'])):
     x=.8+(i%3)*4.1;y=1.95+(i//3)*2.35;panel(x,y,3.85,2.12);fig(id,x+.2,y+.35,1.35,1.35);txt(x+1.75,y+.7,1.95,.8,label,20,True)
   elif key=='capability-hub':
    panel(4.8,2.6,3.7,3.4);item('platform','Gemensam plattform',5,2.85,3.3,2.9)
    for id,label,x,y in [('api','Integration',.9,2),('database','Data',.9,4.4),('security','Säkerhet',9.65,2),('automation','Automation',9.65,4.4)]:item(id,label,x,y,2.7,2.25)
   elif key=='pipeline':
    for i,(id,label) in enumerate(zip(p['figures'],['IT-stöd','Händelser','Datalagring','Analys'])):
     x=.7+i*3.1;item(id,label,x,2.7,2.65,3); 
     if i<3:arrow(x+2.7,3.65,.35)
   else:
    item('application','IT-stöd',.8,3.25,2.5,2.6);arrow(3.4,4.1,.65);item('database','Gemensam data',4.25,3.25,2.7,2.6)
    for i,(id,label) in enumerate(zip(p['figures'][2:],['Analys','AI-assistent','API'])):
     y=2+i*1.55;panel(8.5,y,4,1.35);fig(id,8.7,y+.1,1.15,1.15);txt(10.05,y+.42,2.2,.6,label,19,True)
     a=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,*map(Inches,(7.05,4.25,8.45,y+.67)));a.line.color.rgb=rgb(t['accent']);a.line.width=Pt(2)
   text(s,.65,7.02,12,.3,'IT PRESENTATION CREATOR  /  '+p['composition'],t['muted'],11)
 r.save(path)
if __name__=='__main__':generate(ROOT/'examples/visualization-catalog.pptx')
