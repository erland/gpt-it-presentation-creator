from pathlib import Path
import sys
import yaml
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/itpc'))
from render import render
def generate(path):
    icons=yaml.safe_load((ROOT/'knowledge/figures/professional-icons.yaml').read_text())['icons']
    ids=sorted(icons)
    slides=[]
    for start in range(0,len(ids),15):
        objects=[dict(type='text',x=.6,y=.35,w=12,h=.6,text='Professionella ikoner',size=30,bold=True)]
        for i,key in enumerate(ids[start:start+15]):
            x=.6+(i%5)*2.45;y=1.2+(i//5)*1.95
            objects.extend([dict(type='professional-icon',icon=key,x=x+.65,y=y,w=1.1,h=1.1,id=key,color='primary'),dict(type='text',x=x,y=y+1.15,w=2.4,h=.65,text=key.replace('/','/\n',1),size=12,align='center')])
        slides.append(dict(objects=objects))
    render(dict(slides=slides),path)
if __name__=='__main__':generate(ROOT/'examples/figure-catalog.pptx')
