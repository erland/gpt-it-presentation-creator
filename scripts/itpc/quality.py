"""Conservative model checks and actual slide previews; no claim of aesthetic scoring."""
import argparse, copy, json, shutil, subprocess, tempfile
from pathlib import Path
from figures import THEMES
from render import render
import yaml

def contrast(a,b):
    def lum(h):
        c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
        return sum(w*(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4) for w,v in zip((.2126,.7152,.0722),c))
    x,y=sorted((lum(a),lum(b)));return (y+.05)/(x+.05)

def audit(model):
    issues=[]; W,H=model.get('size',[13.333,7.5])
    for n,s in enumerate(model['slides']):
        t=THEMES[s.get('theme',model.get('theme','executive-clean'))]; bg=s.get('background','background')
        def col(v):return t.get(v,v)
        def walk(objects,prefix=()):
            boxes=[]
            for i,o in enumerate(objects):
                path=prefix+(i,); k=o['type']
                def flag(code,detail):issues.append(dict(slide=n,path=list(path),code=code,detail=detail))
                if k=='group':walk(o['children'],path);continue
                if k=='line':continue
                x,y,w,h=(o[a] for a in ('x','y','w','h'))
                if min(x,y)<0 or min(w,h)<=0 or x+w>W+.001 or y+h>H+.001:flag('bounds','Object outside slide')
                if 'text' in o:
                    size=o.get('size',20); pad=o.get('padding',0)
                    if size<14:flag('small_text','Below 14 pt')
                    if contrast(col(o.get('color','text')),col(o.get('fill','surface') if k=='shape' else bg)) < (3 if size>=24 or size>=18 and o.get('bold') else 4.5):flag('contrast','Low contrast against assumed background')
                    # Approximate only: actual font metrics and wrapping vary by renderer.
                    import math
                    lines=sum(max(1,math.ceil(len(l)*size*.48/max(1,(w-2*pad)*72))) for l in o['text'].split('\n'))
                    if lines*size*1.2>(h-2*pad)*72:flag('text_fit','Estimated text overflow; inspect render')
                if not o.get('allow_overlap'):
                    for j,a,b,c,d in boxes:
                        area=max(0,min(x+w,a+c)-max(x,a))*max(0,min(y+h,b+d)-max(y,b))
                        if area>.12*min(w*h,c*d):flag('overlap',f'Possible overlap with sibling {j}')
                    boxes.append((i,x,y,w,h))
        walk(s['objects'])
    return issues

def correct(model):
    result=copy.deepcopy(model)
    for issue in audit(result):
        s=result['slides'][issue['slide']]; o=s['objects'][issue['path'][0]]
        for i in issue['path'][1:]:o=o['children'][i]
        if issue['code']=='contrast':
            t=THEMES[s.get('theme',result.get('theme','executive-clean'))]; bg=o.get('fill','surface') if o['type']=='shape' else s.get('background','background'); bg=t.get(bg,bg)
            o['color']=max(('000000','FFFFFF'),key=lambda c:contrast(c,bg))
    return result

def previews(pptx,out):
    out.mkdir(parents=True,exist_ok=True)
    if not shutil.which('libreoffice') or not shutil.which('pdftoppm'):raise RuntimeError('Preview requires LibreOffice and Poppler')
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['libreoffice','-env:UserInstallation='+Path(d,'profile').as_uri(),'--headless','--convert-to','pdf','--outdir',d,str(pptx.resolve())],check=True,timeout=90,capture_output=True)
        subprocess.run(['pdftoppm','-r','110','-png',str(Path(d,pptx.stem+'.pdf')),str(out/'slide')],check=True,timeout=90,capture_output=True)
    return sorted(out.glob('slide-*.png'))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('model',type=Path);p.add_argument('output',type=Path);p.add_argument('--correct',action='store_true');a=p.parse_args();m=yaml.safe_load(a.model.read_text());a.output.mkdir(parents=True,exist_ok=True)
    before=audit(m);m=correct(m) if a.correct else m
    (a.output/'report.json').write_text(json.dumps({'before':before,'after':audit(m),'visual_review':'pending'},indent=2));(a.output/'model.yaml').write_text(yaml.safe_dump(m,allow_unicode=True));render(m,a.output/'deck.pptx',a.model.parent);previews(a.output/'deck.pptx',a.output/'previews')
