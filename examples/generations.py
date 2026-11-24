import sys,yaml,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts/itpc'))
from render import render,transform_objects
S=100; navy='101C40'; blue='0876BD'; purple='78259B'; green='17812D'; cols=[blue,purple,green]
O=[]
def b(x,y,w,h):return dict(x=x/S,y=y/S,w=w/S,h=h/S)
def sh(x,y,w,h,f,stroke=None,kind='round',grad=None):
 o=dict(type='shape',shape=kind,**b(x,y,w,h),fill=f,roundness=.12,stroke_pt=.7,allow_overlap=True)
 if stroke:o['stroke']=stroke
 if grad:o['gradient']=grad
 O.append(o)
def tx(x,y,w,h,t,s=20,bold=False,c=navy,center=False):O.append(dict(type='text',**b(x,y,w,h),text=t,size=s*.72,bold=bold,color=c,align='center' if center else 'left',font='Arial',allow_overlap=True))
def ic(n,x,y,w,h,c=navy):O.append(dict(type='icon',icon=n,**b(x,y,w,h),color=c,allow_overlap=True))
def ln(x,y,X,Y,c=navy,arrow=False):O.append(dict(type='line',**{'from':[x/S,y/S],'to':[X/S,Y/S]},color=c,stroke_pt=1.5,arrow=arrow))
def group(fn):
 global O
 old=O;O=[];fn();g=dict(type='group',children=O);O=old;O.append(g)
def team(x,y,c):ic('team-workstation',x,y,66,65,c)
def infra(x,y,w):
 sh(x,y,w,54,'D7EAF9','2673A6',grad=['EAF5FD','C5E2F7'])
 for n,k in [('server',.22),('database',.51),('cloud',.79)]:ic(n,x+w*k-24,y+8,48,38)
def platform(x,y,w):
 sh(x,y,w,111,'DDF3D3','63A75C',grad=['F0FBEA','CDEFC5']);tx(x,y+4,w,27,'Utvecklingsplattform',22,True,navy,True)
 for i,(n,t) in enumerate(zip(['layers','database','network','shield','chart'],['Körmiljö','Data','Integration','Säkerhet','Övervakning'])):
  a=x+12+i*(w-24)/5;cw=(w-24)/5-6;sh(a,y+36,cw,64,'F7FFF3');ic(n,a+cw/2-17,y+41,34,32,'16752C');tx(a,y+77,cw,19,t,13,True,navy,True)
def panel(i):
 c=['174B75','0069B5','25813A','8140A3'][i]; titles=['Det sammanhållna IT-stödet','Tjänsteorienterad IT','Plattformsbaserad IT','Tjänstemannadriven utveckling'];sh(0,0,748,496,'F5F9FC',c,grad=['FFFFFF','EDF4FA']);sh(0,0,748,57,c,grad=[c,['103A60','00549A','17682D','6B318C'][i]]);ic(['server','network','layers','team'][i],38,9,53,40,'FFFFFF');tx(115,8,625,45,f'Generation {i+1} – {titles[i]}',29 if i<3 else 27,True,'FFFFFF'); split=475 if i<2 else 525;ln(split,77,split,472,'9AB3C7');rx=split+13;rw=735-rx
 for j,(label,body) in enumerate([('Löser:',['Samlad IT','Snabb parallell\nutveckling','Självservice\ngenom\nplattformar','Bred\nutvecklingskraft'][i]),('Utmaning:',['Svårt att\nförändra stora\nIT-stöd','Snabb applikations-\nutveckling –\ntrögrörlig\ninfrastruktur','Kräver satsning\npå plattform','Många lösningar\natt hålla ihop'][i])]):
  y=94+j*133;sh(rx,y,rw,118 if j==0 else 176,'E8F0F8',grad=['F0F5FA','E3EDF8']);ic('check-status' if j==0 else 'warning-status',rx+9,y+12,40,40,'55B924' if j==0 else 'EBA900');tx(rx+61,y+11,rw-66,31,label,24,True,'101010');tx(rx+61,y+43,rw-66,130,body,19 if i==1 else 20 if i==0 else 18,False,'101010')
 if i==0:
  team(216,65,c);ln(249,130,249,157,arrow='both');sh(52,158,397,177,'CBE4F7','176AA7',grad=['E3F1FC','BCDDF5']);tx(52,163,397,31,'Stort IT-stöd',25,True,navy,True)
  for j in range(6):
   x=72+j%2*186;y=203+j//2*41;sh(x,y,174,36,'E6F3FC','4B9AC6');tx(x,y+6,174,25,'Delsystem '+chr(65+j),18,False,navy,True)
  ln(249,336,249,366,arrow='both')
 elif i in (1,2):
  xs=[45,190,335] if i==1 else [54,207,360]
  for k,x in enumerate(xs):
   cc=cols[k];team(x+30,65,cc);ln(x+63,130,x+63,153,arrow='both');h=181 if i==1 else 89;sh(x,154,127,h,['E5F4FD','F3E8FA','E8F7E5'][k],cc)
   for j in range(10 if i==1 else 5):
    xx=x+20+(j%2)*59 if i==1 else x+16+(j%3)*35;yy=165+(j//2)*33 if i==1 else 164+(j//3)*30;sh(xx,yy,23,22,['A8D9F7','D9B6EE','BCEAB5'][k],cc,'hex')
   tx(x,154+h-23,127,21,'•••',18,True,navy,True);ln(x+63,154+h,x+63,366 if i==1 else 273,arrow='both')
   if i==1:
    for j in range(4):ln(x+53,190+j*33,x+75,205+j*33,arrow='both')
  if i==1:
   for x in xs[:2]:
    for j in range(4):ln(x+115,187+j*33,x+151,206+j*26,arrow='both')
  else:group(lambda:platform(34,274,474));ln(271,386,271,416,arrow='both')
 else:
  for j in range(8):ic('person-solid',53+j*38,69,35,32,purple)
  sh(25,100,345,35,'E8D9F3');tx(25,107,345,23,'Verksamhetens medarbetare',17,True,navy,True);team(422,60,blue);sh(400,115,110,25,'E8D9F3');tx(400,117,110,22,'IT-team',15,True,navy,True)
  for j,(n,t) in enumerate(zip(['robot','sparkles','cube','settings','layers'],['AI-assistenter','AI-agenter','Applikationer','Automationer','Enterprise IT'])):
   x=[25,119,213,307,400][j];ln(x+43,140,x+43,164,arrow='both');sh(x,165,87 if j<4 else 110,72,'F1E7F8',purple);ic(n,x+24,172,39,32,purple);tx(x,209,87 if j<4 else 110,28,t,13,False,navy,True);ln(x+43,238,x+43,273,arrow='both')
  group(lambda:platform(26,274,486));ln(269,386,269,416,arrow='both')
 if i<2:
  sh(41,368,420,38,'D8EBFA','176AA7');ic('settings',90,372,31,30);tx(139,375,318,27,'Konfigurera plattformar/infrastruktur',16,True);ln(251,407,251,427,arrow='both');group(lambda:infra(41,428,420))
 else:group(lambda:infra(32,416,477))

def build():
 global O
 panels=[]
 for i in range(4):
  O=[];panel(i);panels.append(O)
 slides=[dict(background='FFFFFF',objects=[dict(type='group',children=transform_objects(p,1,.12+(i%2)*7.60,.12+(i//2)*5.12)) for i,p in enumerate(panels)])]
 for p in panels:slides.append(dict(background='FFFFFF',objects=[dict(type='group',children=transform_objects(p,1.99,.24,.18))]))
 return dict(size=[15.36,10.24],slides=slides)
if __name__=='__main__':
 m=build();(ROOT/'examples/generations.yaml').write_text(yaml.safe_dump(m,allow_unicode=True,sort_keys=False));render(m,ROOT/'examples/generations.pptx')
