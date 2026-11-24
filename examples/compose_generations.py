"""Recompose the four panels once, then reuse at two scales."""
import sys,yaml,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts/itpc'))
from render import render,transform_objects
from quality import previews

def build():
 m=yaml.safe_load((ROOT/'examples/professional-generations.yaml').read_text()); panels=[]
 for i,g in enumerate(m['slides'][0]['objects']):
  p=transform_objects(g['children'],1,-(.12+i%2*7.60),-(.12+i//2*5.12)); accent=['314F67','007F87','557B37','A34E35'][i]
  for j,o in enumerate(p):
   if j==0:o.update(fill='FFFFFF',stroke=accent,roundness=.035)
   if j==1:o.update(fill=accent,roundness=.16)
   if j in (5,9):o.update(fill='F0F4F7',roundness=.12)
   if j==3:o.update(size=20 if i<3 else 18.6,y=.10,h=.42,valign='middle')
   if j in (7,11):o.update(size=17.5)
   if j in (8,12):o.update(size=14 if i<2 else 13.5,h=.70 if j==8 else 1.25)
   if i==3 and o.get('icon')=='team-filled':o.update(y=.62,h=.49,w=.55,x=4.275)
  def clean(os):
   for o in os:
    if o['type']=='group':clean(o['children']);continue
    if 'gradient' in o:
     o.pop('gradient')
    if o['type']=='text':o['valign']='middle' if o.get('align')=='center' else o.get('valign','top')
    if o.get('icon')=='phosphor/bold/network':o['icon']='phosphor/bold/network'
  clean(p)
  # Fit explanation cards to their actual line count, preserving padding.
  for card,body in ((5,8),(9,12)):
   lines=p[body]['text'].count('\n')+1
   p[body]['h']=max(.36,lines*.26+.10)
   p[card]['h']=p[body]['y']-p[card]['y']+p[body]['h']+.12
  # Keep a visible gap between the two cards.
  shift=max(0,p[5]['y']+p[5]['h']+.12-p[9]['y'])
  for j in (9,10,11,12):p[j]['y']+=shift
  # Compose a smooth professional people icon with a separate workstation.
  for o in p[:]:
   if o.get('icon')=='team-filled':
    x,y,w,h=(o[k] for k in ('x','y','w','h')); c=o.get('color','text')
    p[p.index(o)]={'type':'group','children':[
      dict(type='professional-icon',icon='phosphor/fill/users',x=x,y=y,w=w,h=h*.59,color=c),
      dict(type='shape',shape='round',x=x+w*.24,y=y+h*.61,w=w*.52,h=h*.30,fill='FFFFFF',stroke=c,stroke_pt=1.7,roundness=.08),
      dict(type='line',**{'from':[x+w*.5,y+h*.91],'to':[x+w*.5,y+h*.98]},color=c,stroke_pt=1.5),
      dict(type='line',**{'from':[x+w*.35,y+h*.98],'to':[x+w*.65,y+h*.98]},color=c,stroke_pt=1.5)]}
  # Align service nodes symmetrically and connect actual node edges.
  if i==1:
   for a,b in [(16,35),(35,54)]:
    for row in range(4):
     src=p[a+2*row+1]; dst=p[b+2*[2,0,3,1][row]]
     line=p[70+(0 if a==16 else 4)+row]
     line.update({'from':[src['x']+src['w']+.025,src['y']+src['h']/2],'to':[dst['x']-.025,dst['y']+dst['h']/2],'stroke_pt':1.25})
  if i==2:
   for start in (16,26,36):
    left=p[start]['x']; top=p[start]['y']
    for k,(dx,dy) in enumerate(((.175,0),(.525,0),(0,.30),(.35,.30),(.70,.30))):
     p[start+k].update(x=left+dx,y=top+dy)
  def polish(os):
   for o in os:
    if o['type']=='group':polish(o['children'])
    elif o.get('icon') in ('phosphor/bold/hard-drives','phosphor/bold/database','phosphor/bold/cloud') and o['h']<.4:
     o.update(x=o['x']-.06,y=o['y']-.035,w=o['w']+.12,h=o['h']+.07)
  polish(p);panels.append(p)
 m['slides']=[dict(background='FFFFFF',objects=[dict(type='group',children=transform_objects(p,1,.12+i%2*7.60,.12+i//2*5.12)) for i,p in enumerate(panels)])]+[dict(background='FFFFFF',objects=[dict(type='group',children=transform_objects(p,1.99,.24,.18))]) for p in panels];return m
if __name__=='__main__':
 m=build();(ROOT/'examples/composed-generations.yaml').write_text(yaml.safe_dump(m,allow_unicode=True));render(m,ROOT/'examples/composed-generations.pptx');previews(ROOT/'examples/composed-generations.pptx',Path('/tmp/8f-preview'))
