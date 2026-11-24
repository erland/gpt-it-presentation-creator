from pathlib import Path
import sys,yaml
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts/itpc'))
from render import render
from quality import audit,previews
P=Path(__file__).parent

def txt(x,y,w,h,text,size=20,**kw):return dict(type='text',x=x,y=y,w=w,h=h,text=text,size=size,**kw)
def fig(id,x,y,w,h):return dict(type='figure',figure=id,x=x,y=y,w=w,h=h)
def shape(x,y,w,h,fill):return dict(type='shape',x=x,y=y,w=w,h=h,fill=fill,allow_overlap=True)
def line(x,y,x2,y2,arrow=False):return {'type':'line','from':[x,y],'to':[x2,y2],'arrow':arrow,'stroke_pt':2}
def header(k,t):return [txt(.65,.35,12,.32,k,14,color='muted',bold=True),txt(.65,.85,12,1,t,32,bold=True)]
def footer(t):return [line(.65,6.7,12.65,6.7),txt(.65,6.85,12,.42,t,16,bold=True)]
def slide(o):return {'objects':o}
def decks():
 o=header('STRATEGISK FÖRFLYTTNING','Fyra generationer av IT-leverans')
 for i,(f,t,d) in enumerate([('legacy','Systemdrift','Beställ teknik'),('microservices','Komponenter','Samordna tjänster'),('platform','Plattformar','Självservice för team'),('ai-team','Verksamhetsdriven','Skapa med AI-stöd')]):
  x=.65+i*3.08;o += [txt(x,2.0,2.8,.65,f'0{i+1}',32,color='muted',bold=True),fig(f,x+.35,2.8,2.15,2.15),txt(x,5.1,2.85,.5,t,19,bold=True),txt(x,5.7,2.85,.65,d,17)]
  if i<3:o.append(line(x+2.65,3.8,x+3.03,3.8,True))
 a=header('ANSVAR OCH HANDLINGSUTRYMME','Från beställare till digital självständighet')+[fig('legacy',.8,2.1,3.2,3.2),fig('platform',5.0,2.1,3.2,3.2),fig('ai-team',9.2,2.1,3.2,3.2),line(4.1,3.7,4.8,3.7,True),line(8.3,3.7,9,3.7,True),txt(.8,5.5,3.2,.85,'IT levererar teknik',22,bold=True,align='center'),txt(5,5.5,3.2,.85,'Team nyttjar förmågor',22,bold=True,align='center'),txt(9.2,5.5,3.2,.85,'Verksamheten skapar',22,bold=True,align='center')]
 yield 'generationer',{'theme':'executive-clean','slides':[slide(o+footer('Förflyttningen handlar om ansvar och självständighet – inte bara teknik.')),slide(a)]}
 o=header('AI I KÄRNVERKSAMHETEN','Från traditionella IT-stöd till integrerad AI')+[fig('application',1.0,2.5,3.0,3.0),txt(.8,5.65,3.4,.65,'Fördefinierade funktioner',20,align='center'),line(4.5,4,5.6,4,True),dict(fig('ai-environment',6.0,1.8,5.9,3.8),fit='contain'),txt(6,5.65,5.9,.65,'AI samverkar med data och IT-stöd',20,align='center')]
 a=header('TRE KOMPLETTERANDE FORMER','AI får olika roller beroende på uppgiften')
 for i,(f,t,d) in enumerate([('assistant','Assistent','Stödjer människans arbete'),('agent','Agent','Utför avgränsade uppgifter'),('model','Specialiserad AI','Exempelvis transkribering')]):
  x=.8+i*4.2;a += [fig(f,x+.7,2.1,2.4,2.4),txt(x,4.8,3.8,.6,t,24,bold=True,align='center'),txt(x,5.5,3.8,.85,d,19,align='center')]
 yield 'ai',{'theme':'modern-technology','slides':[slide(o+footer('AI kompletterar befintliga IT-stöd och arbetsprocesser.')),slide(a)]}
 o=header('GEMENSAMMA FÖRMÅGOR','Plattformen gör självservice möjlig')
 for i,(f,t) in enumerate([('application','IT-stöd'),('analytics','Analysstöd'),('agent','AI-stöd')]):
  x=1.1+i*4.1;o += [fig(f,x+.7,1.95,1.65,1.65),txt(x,3.65,3.1,.4,t,20,bold=True,align='center')]
 o += [dict(type='shape',x=.65,y=4.25,w=12,h=.75,fill='primary',text='Gemensam självservice och automatisering',color='on_primary',size=24,align='center',valign='middle')]
 for i,(f,t) in enumerate([('cloud','Körmiljö'),('database','Data'),('api','Integration'),('security','Säkerhet'),('monitor','Övervakning')]):
  x=.85+i*2.45;o += [fig(f,x+.6,5.15,1.0,1.0),txt(x,6.2,2.2,.4,t,16,align='center')]
 a=header('OPERATIV MODELL','Team skapar – plattformen möjliggör')+[fig('team',1,2.2,3.4,3.4),line(4.6,3.8,6.1,3.8,True),dict(fig('platform',6.4,2.0,5.3,3.8),fit='contain'),txt(.8,5.85,3.8,.6,'Ansvar för IT-stödet',22,bold=True,align='center'),txt(6.2,5.85,5.7,.6,'Återanvändbara tjänster',22,bold=True,align='center')]
 yield 'plattform',{'theme':'editorial-professional','slides':[slide(o),slide(a)]}
if __name__=='__main__':
 for name,m in decks():
  (P/f'{name}.yaml').write_text(yaml.safe_dump(m,allow_unicode=True));print(name,audit(m));out=P/f'{name}.pptx';render(m,out);previews(out,Path('/tmp/it8-preview')/name)
