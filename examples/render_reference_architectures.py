"""Render and structurally inspect the four DEV-012D architecture references.

Usage: python examples/render_reference_architectures.py --output-dir build/reference-review --with-previews
The model remains a standalone editable slide composition, not a new icon library.
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from pptx import Presentation
from pptx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/itpc'))
from render import render
from quality import audit,previews

SOURCE=ROOT/'examples/reference-architectures.json'

def load_model():return json.loads(SOURCE.read_text(encoding='utf-8'))

def inspect(pptx):
    prs=Presentation(pptx)
    result=[]
    for index,slide in enumerate(prs.slides,1):
        images=list(slide._element.iter(qn('p:pic')))
        assert not images, f'Slide {index} contains raster pictures'
        types=Counter(str(sh.shape_type) for sh in slide.shapes)
        vectors=len(list(slide._element.iter(qn('a:custGeom'))))
        assert vectors>=3, f'Slide {index} has too few editable custom geometries'
        assert any(sh.has_text_frame and sh.text for sh in slide.shapes)
        assert all(sh.left>=0 and sh.top>=0 and sh.left+sh.width<=prs.slide_width+1000 and sh.top+sh.height<=prs.slide_height+1000 for sh in slide.shapes), f'Slide {index} has objects outside slide'
        result.append({'slide':index,'top_level_shapes':len(slide.shapes),'editable_custom_geometries':vectors,'raster_pictures':len(images),'dashed_elements':len(list(slide._element.iter(qn('a:prstDash')))),'transparent_fills':len(list(slide._element.iter(qn('a:alpha')))),'shape_types':dict(types)})
    assert len(result)==4
    assert result[1]['dashed_elements']>=4
    assert all(row['transparent_fills']>=2 for row in result)
    return result

def create(output,with_previews=False):
    output.mkdir(parents=True,exist_ok=True)
    model=load_model()
    assert len(model['slides'])==4
    issues=audit(model)
    assert not issues, f'Unexpected model audit issues: {issues[:3]}'
    pptx=output/'reference-architectures.pptx'
    render(model,pptx)
    pages=inspect(pptx)
    result={'slides':pages,'model_audit_findings':issues,'visual_status':'not_determined_by_automated_checks'}
    if with_previews:
        images=previews(pptx,output/'previews')
        assert len(images)==4
        from PIL import Image
        sheet=Image.new('RGB',(2400,1350),'white')
        for index,path in enumerate(images):
            with Image.open(path) as im:
                im=im.convert('RGB')
                assert im.width>=1000 and im.height>=550
                im.thumbnail((1200,675))
                sheet.paste(im,((index%2)*1200,(index//2)*675))
        sheet.save(output/'contact-sheet.png')
        result['rendered_previews']=[str(p.relative_to(output)) for p in images]
    (output/'technical-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--with-previews',action='store_true')
    args=p.parse_args()
    result=create(args.output_dir,args.with_previews)
    print(f'PASS: {len(result["slides"])} editable reference slides; raster images: 0; model-audit findings: 0')
