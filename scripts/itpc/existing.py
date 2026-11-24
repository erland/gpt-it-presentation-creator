"""Selective edits to existing PPTX; never rebuild unrelated package parts."""
import argparse,json,hashlib,math,zipfile,io
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from lxml import etree

def inspect(source):
    p=Presentation(source); slides=[]
    for i,s in enumerate(p.slides,1):
        shapes=[]
        for o in s.shapes:
            shapes.append(dict(id=o.shape_id,name=o.name,type=str(o.shape_type),text=o.text if o.has_text_frame else None,box=[round(v/914400,3) for v in (o.left,o.top,o.width,o.height)],outside=o.left<0 or o.top<0 or o.left+o.width>p.slide_width or o.top+o.height>p.slide_height))
        slides.append(dict(slide=i,shapes=shapes))
    return dict(size=[p.slide_width/914400,p.slide_height/914400],slides=slides,profile='Preserve original theme, masters and layouts; inspect rendered colors and typography.')

def revise(source,output,edits):
    source,output=Path(source),Path(output)
    if source.resolve()==output.resolve() or output.exists():raise ValueError('Use a new output file')
    p=Presentation(source); changed={}
    for e in edits:
        if set(e)-{'slide','id','box','font_size','color'}:raise ValueError('Unsupported edit')
        n=e['slide'];
        if not isinstance(n,int) or not 1<=n<=len(p.slides):raise ValueError('Invalid slide')
        s=p.slides[n-1]; o=next((o for o in s.shapes if o.shape_id==e['id']),None)
        if o is None:raise ValueError('Unknown shape')
        if 'box' in e:
            x,y,w,h=e['box']; W,H=p.slide_width/914400,p.slide_height/914400
            if not all(map(math.isfinite,[x,y,w,h])) or min(x,y)<0 or min(w,h)<=0 or x+w>W+.0001 or y+h>H+.0001:raise ValueError('Invalid bounds')
            o.left,o.top,o.width,o.height=map(Inches,[x,y,w,h])
        if 'font_size' in e or 'color' in e:
            if not o.has_text_frame:raise ValueError('Not text')
            for para in o.text_frame.paragraphs:
                for run in para.runs:
                    if 'font_size' in e:
                        if not 8<=e['font_size']<=96:raise ValueError('Invalid font size')
                        run.font.size=Pt(e['font_size'])
                    if 'color' in e:run.font.color.rgb=RGBColor.from_string(e['color'])
        changed[str(s.part.partname).lstrip('/')]=s.part.blob
    # Copy original ZIP entries verbatim in content, replacing only selected slide XML.
    with zipfile.ZipFile(source) as a,zipfile.ZipFile(output,'x') as b:
        for info in a.infolist():b.writestr(info,changed.get(info.filename,a.read(info.filename)))
    return sorted(changed)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--edits',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    if a.edits:
        if not a.output:p.error('--output required')
        print(json.dumps(revise(a.source,a.output,json.loads(a.edits.read_text()))))
    else:print(json.dumps(inspect(a.source),ensure_ascii=False,indent=2))
