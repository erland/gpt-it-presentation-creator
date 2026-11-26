"""Conservative model checks and actual slide previews; no claim of aesthetic scoring."""
import argparse, copy, json, math, shutil, subprocess, tempfile
from pathlib import Path
from figures import THEMES
from render import render
import yaml

def contrast(a,b):
    def lum(h):
        c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
        return sum(w*(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4) for w,v in zip((.2126,.7152,.0722),c))
    x,y=sorted((lum(a),lum(b)));return (y+.05)/(x+.05)

def _rect(o):
    return o['x'],o['y'],o['w'],o['h']

def _intersects(first,second):
    x,y,w,h=_rect(first);a,b,c,d=_rect(second)
    return max(x,a)<min(x+w,a+c) and max(y,b)<min(y+h,b+d)

def _covers(background,foreground):
    """True only when a later text box is geometrically inside an earlier fill."""
    if not all(k in background for k in ('x','y','w','h')):return False
    x,y,w,h=_rect(background);a,b,c,d=_rect(foreground)
    return x<=a and y<=b and x+w>=a+c and y+h>=b+d

def _blend(foreground,background,alpha):
    values=[round(int(foreground[i:i+2],16)*alpha+int(background[i:i+2],16)*(1-alpha)) for i in (0,2,4)]
    return ''.join(f'{v:02X}' for v in values)

def _fill_over(background,base,col):
    """Blend only known solid fills; unsupported gradients remain conservative."""
    fill=background.get('fill','surface')
    if fill=='none':return base
    if 'gradient' in background:return None
    value=col(fill);opacity=background.get('fill_opacity',1)
    if not isinstance(opacity,(int,float)) or not math.isfinite(opacity) or not 0<=opacity<=1:return None
    return _blend(value,base,opacity)

def _background_for_text(o,preceding,slide_bg,col):
    if o['type']=='shape' and o.get('fill','surface')!='none':
        return _fill_over(o,slide_bg,col)
    # A later opaque or translucent shape might cover the earlier background.
    # A containing series is composited in the same order as rendered.
    backdrop=slide_bg
    for item in preceding:
        if item['type']!='shape' or not _intersects(item,o):continue
        if not _covers(item,o):return None
        backdrop=_fill_over(item,backdrop,col) if backdrop is not None else None
    return backdrop

def estimate_text_lines(value,width_pt,size_pt):
    """Word-aware, pure-Python estimate; renderer-specific proof still needs PDF."""
    if width_pt<=0:return float('inf')
    def extent(s):
        narrow="ilI1.,:;!|'` "
        wide="MW@%&Q"
        return sum(size_pt*(.26 if c in narrow else .86 if c in wide else
                           .64 if c.isupper() else .52) for c in s)
    count=0
    for paragraph in value.split('\\n'):
        words=paragraph.split()
        if not words:count+=1;continue
        used=0
        for word in words:
            need=extent(word)
            sep=extent(' ') if used else 0
            if used and used+sep+need>width_pt:
                count+=1;used=need
            else:used+=sep+need
            if need>width_pt:
                excess=math.ceil(need/width_pt)
                count+=excess-1
                used=need-(excess-1)*width_pt
        count+=1
    return count

def audit(model):
    issues=[];W,H=model.get('size',[13.333,7.5])
    for n,s in enumerate(model['slides']):
        t=THEMES[s.get('theme',model.get('theme','executive-clean'))];bg=s.get('background','background')
        def col(v):return t.get(v,v)
        slide_bg=col(bg)
        def walk(objects,prefix=()):
            boxes=[];preceding=[]
            for i,o in enumerate(objects):
                path=prefix+(i,);k=o['type']
                def flag(code,detail):issues.append(dict(slide=n,path=list(path),code=code,detail=detail))
                if k=='group':
                    walk(o['children'],path)
                    continue
                if k=='line':continue
                x,y,w,h=(o[a] for a in ('x','y','w','h'))
                if min(x,y)<0 or min(w,h)<=0 or x+w>W+.001 or y+h>H+.001:flag('bounds','Object outside slide')
                if 'text' in o:
                    size=o.get('size',20);pad=o.get('padding',0)
                    if size<14:flag('small_text','Below 14 pt')
                    background=_background_for_text(o,preceding,slide_bg,col)
                    limit=3 if size>=24 or (size>=18 and o.get('bold')) else 4.5
                    if background is None:
                        flag('contrast_unknown','Text is over an unsupported/complex fill; inspect render')
                    elif contrast(col(o.get('color','text')),background)<limit:
                        flag('contrast','Low contrast against actual modeled background')
                    # Word-aware estimate, not a substitute for actual PDF line geometry.
                    lines=estimate_text_lines(o['text'],max(0,(w-2*pad)*72),size)
                    if lines*size*1.2>(h-2*pad)*72:flag('text_fit','Estimated text overflow; inspect render')
                if not o.get('allow_overlap'):
                    for j,a,b,c,d in boxes:
                        area=max(0,min(x+w,a+c)-max(x,a))*max(0,min(y+h,b+d)-max(y,b))
                        if area>.12*min(w*h,c*d):flag('overlap',f'Possible overlap with sibling {j}')
                    boxes.append((i,x,y,w,h))
                preceding.append(o)
        walk(s['objects'])
    return issues

def correct(model):
    result=copy.deepcopy(model)
    for issue in audit(result):
        if issue['code']!='contrast':continue
        s=result['slides'][issue['slide']]
        t=THEMES[s.get('theme',result.get('theme','executive-clean'))]
        col=lambda v:t.get(v,v)
        objects=s['objects'];o=objects[issue['path'][0]]
        if len(issue['path'])>1:
            # Keep nested editing conservative: the source group may have backgrounds
            # outside it and requires a proper whole-slide visibility analysis.
            continue
        bg=_background_for_text(o,objects[:issue['path'][0]],col(s.get('background','background')),col)
        if bg is not None:o['color']=max(('000000','FFFFFF'),key=lambda c:contrast(c,bg))
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
