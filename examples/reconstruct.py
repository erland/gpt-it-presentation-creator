from pathlib import Path
import sys,yaml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts/itpc'))
from render import render
O=[]; S=115.2
nav='102746'; teal='086B60'; dark='101B20'; blue='22536C'; light='D8F1F7'; green='D7F5EF'
def box(x,y,w,h):return dict(x=x/S,y=y/S,w=w/S,h=h/S)
def shape(x,y,w,h,fill,stroke=None,grad=None,round=True):
 o=dict(type='shape',shape='round' if round else 'rect',**box(x,y,w,h),fill=fill,allow_overlap=True,roundness=.13)
 if stroke:o['stroke']=stroke
 if grad:o['gradient']=grad
 O.append(o)
def text(x,y,w,h,v,size=16,bold=False,c=dark,center=False):O.append(dict(type='text',**box(x,y,w,h),text=v,size=size*72/S,bold=bold,color=c,align='center' if center else 'left',font='Arial',allow_overlap=True))
def icon(n,x,y,w=45,h=45,c=nav):O.append(dict(type='icon',icon=n,**box(x,y,w,h),color=c,allow_overlap=True))
def line(x,y,X,Y,c=nav,arrow=False):O.append(dict(type='line',**{'from':[x/S,y/S],'to':[X/S,Y/S]},color=c,stroke_pt=1.4,arrow=arrow))
def tile(x,y,w,h,n,title,sub,c=nav):
 shape(x,y,w,h,light,'60BED1',['C4EBF3','E5F7FA']);icon(n,x+w/2-25,y+8,50,48,c);text(x+3,y+(66 if h>120 else 53),w-6,25,title,19,True,center=True);text(x+4,y+(92 if h>120 else 76),w-8,h-(92 if h>120 else 76),sub,13,center=True)
def note(n,x,y,w,title,sub,c=nav):
 icon(n,x,y+4,43,43,c);text(x+55,y,w-55,42,title,17,True);text(x+55,y+39,w-55,59,sub,15)
text(10,0,1516,64,'Förflyttning till verksamhetsintegrerad AI',55,True,nav,True)
text(20,65,1496,34,'Från isolerade AI-lösningar till integrerade AI-assistenter, agenter och AI-funktioner som använder data och funktioner i verksamhetens IT-stöd',23,False,blue,True)
shape(7,134,615,490,'F3F8FC','7CABC6',['FFFFFF','E5F2FA']);shape(749,134,784,498,'F0FAF8','75B9AE',['FFFFFF','DFF6F0'])
shape(7,134,615,52,blue,None,['234C68','32647C']);shape(749,134,784,52,teal,None,['00624F','087A68']);text(38,141,575,40,'FRÅN – isolerade AI-lösningar',30,True,'FFFFFF');text(778,140,745,40,'TILL – integrerade AI-assistenter, agenter och AI-funktioner',24,True,'FFFFFF')
tile(22,222,182,145,'document','Dokument-AI','(analys, sammanfattning,\nklassificering)');tile(216,222,172,145,'robot','Specialiserad AI','(t.ex. analys, prediktion,\nklassificering)')
line(113,367,113,395);line(302,367,302,395);line(113,395,302,395);line(210,395,210,421,arrow=True)
shape(35,422,346,74,'D4EBF5');icon('database',82,432,54,54);text(165,435,207,54,'Separata dokument\noch datakopior',20)
line(214,497,214,519,arrow=True);shape(31,519,357,75,'D4EBF5');icon('monitor',50,535,45,45);icon('server',116,535,45,45);text(186,536,195,55,'IT-stöd används\nhuvudsakligen manuellt',18)
line(400,205,400,601,'91B7D0')
for n,y,v in [('settings',205,'Avgränsade\nAI-funktioner\nmed begränsad\nintegration'),('target',298,'Fokus på analys,\nklassificering och\ninnehållsförståelse'),('upload',371,'Information\nkopieras eller\nladdas upp manuellt'),('team',445,'Människor överför\nresultat till andra\nIT-stöd'),('sliders',518,'Separat styrning\noch uppföljning\nper lösning')]:
 icon(n,414,y+7,42,42);text(469,y,145,85,v,15)
# central editable freeform arrow
O.append(dict(type='path',**box(608,244,194,296),points=[[0,17],[55,17],[55,0],[100,46],[55,100],[55,84],[0,84]],closed=True,fill='087E70',allow_overlap=True));text(612,306,160,184,'Förflyttning:\nFrån isolerade\nAI-lösningar till\nintegrerade,\nstyrda och\nåteranvändbara\nAI-förmågor',17,True,'FFFFFF',True)
# right tiles
for x,n,t,sub in [(769,'person','AI-assistenter','(stöd i arbetet)'),(946,'robot','AI-agenter','(utför uppgifter)'),(1117,'spark','Specialiserad AI','(t.ex. transkribering,\nklassificering, tolkning)')]:tile(x,205,165 if x!=1117 else 173,114,n,t,sub)
for x in [853,1028,1205]:line(x,319,x,339)
line(853,339,1205,339);line(1028,339,1028,365,arrow=True)
shape(809,367,450,61,'C1EEEE',None,['C9F3F2','A8E2E3']);icon('network',887,374,51,48,teal);text(949,373,305,26,'Integration och verktyg',22,True,nav);text(949,401,305,23,'MCP · API:er',18,center=True)
for x in [890,1028,1178]:line(x,431,x,461,arrow=True);line(x+5,460,x+5,434,arrow=True)
shape(770,464,521,156,'D2EEF5');text(776,469,509,27,'IT-stöd',23,True,nav,True);text(776,495,509,24,'Läsa information · Utföra åtgärder · Uppdatera data',16,center=True)
for x,n,t,sub in [(781,'database','Data och register',''),(953,'server','Verksamhetssystem','✦ AI-funktioner'),(1125,'settings','Övriga IT-stöd','(t.ex. analys, media, tjänster)\n✦ AI-funktioner')]:
 shape(x,521,160,97,'CBEFF1','63B9C9');icon(n,x+60,528,40,39,teal);text(x+3,568,154,20,t,16,False,center=True);text(x+3,588,154,30,sub,10,False,nav,True)
line(1303,205,1303,616,'80C5BA')
for n,y,t,sub in [('shield',201,'Styrning och\nskyddsräcken','(behörigheter, policy,\ntillåtna åtgärder,\ngodkännande)'),('clipboard',305,'Loggning och\nuppföljning','(spårbarhet, resultat\noch avvikelser)'),('layers',394,'Löst kopplade\nlösningar','(återanvändbara\nintegrationer, MCP)'),('refresh',490,'Kontinuerlig\nutveckling och\nförbättring','(av AI-lösningar\noch IT-stöd)')]:
 icon(n,1317,y+4,48,48,teal);text(1378,y,150,61,t,18,True);text(1378,y+(61 if n=='refresh' else 40),150,60,sub,15)
shape(7,654,1526,121,'D9F5EF',None,['E6F8F7','D1F6EB']);text(35,675,200,85,'Fördelar med\nintegrerad AI',29,True,nav)
for i,(n,v) in enumerate([('rocket','Snabbare\nverksamhets-\nutveckling'),('workflow','Automatiserade\narbetsflöden'),('layers','Återanvändbara\nintegrationer\noch data'),('team','Människa och\nAI i samverkan'),('shield','Kontrollerad\noch spårbar\nAI'),('chart','Större\nverksamhetsnytta\noch flexibilitet')]):
 x=238+i*215;line(x,671,x,750,'62B6B1');icon(n,x+18,682,54,54,teal);text(x+85,678,min(129,1530-x-85),80,v,15)
model=dict(size=[1536/S,786/S],slides=[dict(background='FFFFFF',objects=O)])
if __name__=='__main__':
 p=ROOT/'examples/reconstruction.yaml';p.write_text(yaml.safe_dump(model,allow_unicode=True,sort_keys=False));render(model,ROOT/'examples/reconstruction.pptx')
