"""DEV-012E: three demanding, editable visual compositions.
Free layout primitives only; no custom figure library or raster-based icons.
Usage: python examples/advanced_compositions.py --output-dir build/advanced-review --with-previews
"""
import argparse
import json
import sys
from pathlib import Path
from pptx import Presentation
from pptx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/itpc'))
from render import render
from quality import audit,previews

W,H=13.333,7.5
INK='17344F'
MUTED='526B7D'
WHITE='FFFFFF'
PALE='EAF2F8'
TURQUOISE='187F85'
BLUE='246FA2'
VIOLET='7652B0'
DARK='163653'
LINE='D7E3ED'

def text(x,y,w,h,value,size=16,color=INK,bold=False,align='left'):
    return dict(type='text',x=x,y=y,w=w,h=h,text=value,size=size,color=color,bold=bold,align=align)

def shape(x,y,w,h,fill=WHITE,stroke=None,roundness=.10,opacity=None,**kw):
    result=dict(type='shape',shape='round',x=x,y=y,w=w,h=h,fill=fill,
                roundness=roundness,allow_overlap=True,**kw)
    if stroke: result.update(stroke=stroke,stroke_pt=.9)
    if opacity is not None: result['fill_opacity']=opacity
    return result

def icon(name,x,y,size=.50,color=INK):
    return dict(type='professional-icon',icon='phosphor/regular/'+name,
                x=x,y=y,w=size,h=size,color=color,allow_overlap=True)

def line(x,y,x2,y2,color=BLUE,arrow=True,dashed=False,width=1.7):
    o={'type':'line','from':[x,y],'to':[x2,y2],'color':color,'arrow':arrow,'stroke_pt':width}
    if dashed:o['stroke_dash']='dash'
    return o

def header(num,kicker,title,sub,accent=BLUE):
    return [shape(.47,.33,.07,.49,accent),
            text(.72,.32,11.8,.29,f'{num:02d}   /   {kicker.upper()}',14,MUTED,True),
            text(.69,.77,12,.56,title,23,INK,True),
            text(.70,1.47,11.9,.39,sub,15,MUTED)]

def footer(label):
    return [shape(.66,7.01,12,.02,LINE,roundness=0),
            text(.70,7.09,11.75,.28,label,14,MUTED)]

def component(x,y,w,label,sub,ico,accent=BLUE,light=WHITE):
    return [shape(x,y,w,.79,light,LINE),
            shape(x,y,.065,.79,accent,roundness=0),
            icon(ico,x+.16,y+.18,.40,accent),
            text(x+.70,y+.12,w-.83,.29,label,14.5,INK,True),
            text(x+.70,y+.47,w-.83,.30,sub,14,MUTED)]

def generations():
    o=header(1,'Fyra IT-generationer',
             'Från driftbeställningar till verksamhetsdriven utveckling',
             'Fyra sätt att organisera ansvar, arkitektur och leverans – samma grundläggande teknikbehov.')
    accents=[DARK,BLUE,TURQUOISE,VIOLET]
    labels=[('GEN 1','Monolit','Beställ teknik'),('GEN 2','Microservices','Samordna många delar'),
            ('GEN 3','Plattform','Team får självservice'),('GEN 4','Verksamhetsnära','Skapa med AI-stöd')]
    cards=[('Monolit','En leverans','browser'),('Tjänster & API','Många delar','plugs-connected'),
           ('Produktteam','På plattform','users'),('Verksamhet','Nära behoven','robot')]
    xs=[.66,3.89,7.12,10.35]
    for i,(x,c) in enumerate(zip(xs,accents)):
        w=2.98
        o += [shape(x,2.06,w,4.63,'F5F8FB',LINE),shape(x,2.06,w,.65,c),
              text(x+.17,2.19,w-.34,.29,labels[i][0],14,WHITE,True),
              text(x+.17,2.83,w-.34,.41,labels[i][1],19,INK,True),
              text(x+.17,3.35,w-.34,.28,labels[i][2],14,MUTED),
              shape(x+.19,3.85,w-.38,1.06,WHITE,LINE),
              icon(cards[i][2],x+.38,4.07,.52,c),
              text(x+1.04,4.02,1.65,.33,cards[i][0],14,INK,True),
              text(x+1.04,4.42,1.65,.29,cards[i][1],14,MUTED),
              shape(x+.22,5.20,w-.44,.02,LINE,roundness=0)]
        if i==0:
            o += [icon('hard-drives',x+.40,5.48,.38,c),icon('database',x+1.23,5.48,.38,c),icon('cloud',x+2.06,5.48,.38,c),
                  text(x+.25,5.97,w-.5,.46,'Drift & konfiguration',14,INK,True,'center')]
        elif i==1:
            for k,ix in enumerate(['cube','database','queue']):
                xx=x+.32+k*.82
                o += [shape(xx,5.35,.69,.55,'E8F1F9',LINE),icon(ix,xx+.15,5.42,.36,c)]
            o.append(text(x+.25,5.97,w-.5,.46,'Många beroenden',14,INK,True,'center'))
        elif i==2:
            o += [shape(x+.34,5.42,2.30,.47,'E1F2EE'),icon('stack',x+.49,5.46,.35,c),
                  text(x+1.02,5.52,1.38,.29,'Plattform',14,INK,True),
                  text(x+.25,5.97,w-.5,.46,'Självservice',14,INK,True,'center')]
        else:
            o += [icon('user',x+.48,5.49,.40,c),line(x+1.03,5.67,x+1.73,5.67,c),
                  icon('brain',x+1.88,5.49,.40,c),
                  text(x+.25,5.97,w-.5,.46,'AI integrerad i arbetet',14,INK,True,'center')]
    for i in range(3):
        x=xs[i]+3.00
        o.append(line(x,4.30,x+.16,4.30,MUTED,True,width=1.2))
    o+=footer('Varje generation förändrar ansvar och arbetssätt. Infrastruktur, säkerhet och data behövs i alla fyra.')
    return {'objects':o}

def ai_transition():
    o=header(2,'Verksamhetsintegrerad AI',
             'Från fristående AI-tjänster till intelligenta arbetsflöden',
             'AI-assistenter, AI-agenter, IT-stöd och specialiserad AI har olika roller.',VIOLET)
    o += [shape(.65,2.18,4.70,4.62,'F4F6F9',LINE),
          shape(5.87,2.18,6.80,4.62,'F5F2FB','DCD3EF'),
          shape(.65,2.18,4.70,.52,DARK),shape(5.87,2.18,6.80,.52,VIOLET),
          text(.90,2.31,4.2,.29,'IDAG  /  FRISTÅENDE FUNKTIONER',14,WHITE,True),
          text(6.12,2.31,6.3,.29,'MÅLBILD  /  AI I VERKSAMHETEN',14,WHITE,True),
          text(.96,2.99,3.94,.36,'Människan växlar verktyg',17,INK,True,'center')]
    o += component(1.02,3.63,3.96,'IT-stöd','Ordinarie funktioner','browser',DARK)
    o += component(1.02,4.72,3.96,'AI som separat tjänst','Resultatet flyttas manuellt','chat-circle',DARK)
    o += [line(3.00,4.47,3.00,4.66,MUTED,True,True,1.4),
          text(1.10,5.89,3.76,.50,'Begränsad koppling till process och data',14,MUTED,False,'center')]
    o += [shape(6.15,2.97,3.33,1.12,'ECE7F7'),icon('user',6.39,3.22,.48,VIOLET),
          text(7.02,3.17,2.32,.30,'Medarbetare',16,INK,True),
          text(7.02,3.55,2.32,.28,'Mål och beslut',14,MUTED),
          line(7.83,4.11,7.83,4.38,VIOLET),
          shape(6.15,4.41,3.33,1.01,WHITE,'DCD3EF'),icon('robot',6.38,4.62,.50,VIOLET),
          text(7.03,4.55,2.32,.31,'Assistent / agent',16,INK,True),
          text(7.03,4.91,2.32,.28,'Verktyg och kontroller',14,MUTED)]
    for y,ico,lbl,sub in [(3.03,'brain','Språkmodell','Textstöd'),
                           (4.10,'browser','IT-stöd','Läs / skriv'),
                           (5.17,'waveform','Nisch-AI','Transkribering')]:
        o += [shape(9.75,y,2.64,.93,WHITE,'DCD3EF'),
              icon(ico,9.95,y+.19,.40,VIOLET),
              text(10.52,y+.11,1.66,.29,lbl,14,INK,True),
              text(10.52,y+.49,1.66,.28,sub,14,MUTED)]
    o += [line(9.48,4.90,9.66,4.90,VIOLET),
          line(9.62,3.49,9.62,5.64,VIOLET,False,False,1.4),
          line(9.62,3.49,9.73,3.49,VIOLET),
          line(9.62,5.64,9.73,5.64,VIOLET),
          shape(6.15,5.74,3.33,.67,'E9EEF4'),icon('shield-check',6.36,5.86,.41,DARK),
          text(6.88,5.87,2.40,.46,'MCP · skydd · logg',14,INK,True)]
    o+=footer('IT-stöd kan också använda AI som intern funktion. Specialiserad AI behöver inte vara en assistent.')
    return {'objects':o}

def data_architecture():
    o=header(3,'Data warehouse → Lakehouse',
             'En gemensam datagrund breddar analysmöjligheterna',
             'Två arkitekturmönster jämförs – inget är automatiskt rätt för alla behov.',TURQUOISE)
    o += [shape(.65,2.17,5.74,4.67,'F5F8FB',LINE),
          shape(6.91,2.17,5.74,4.67,'EEF8F6','CDE8E1'),
          shape(.65,2.17,5.74,.55,DARK),shape(6.91,2.17,5.74,.55,TURQUOISE),
          text(.92,2.32,5.10,.31,'TRADITIONELLT DATA WAREHOUSE',14.5,WHITE,True),
          text(7.18,2.32,5.15,.31,'DATA LAKEHOUSE',14.5,WHITE,True)]
    for x,ico,label in [(1.03,'database','IT-data'),(2.71,'file-text','Filer'),(4.38,'browser','IT-stöd')]:
        o += [shape(x,2.98,1.57,.67,WHITE,LINE),icon(ico,x+.14,3.10,.38,BLUE),
              text(x+.60,3.16,.87,.30,label,14,INK,True)]
    o += [line(3.52,3.68,3.52,3.99,BLUE),
          shape(1.38,4.03,4.26,.69,'E5EDF5'),icon('gear',1.70,4.19,.35,BLUE),
          text(2.20,4.18,3.16,.31,'ETL · modellering · kvalitet',14.5,INK,True),
          line(3.52,4.75,3.52,5.04,BLUE),
          shape(1.38,5.08,4.26,.72,'D4E3F0'),icon('database',1.72,5.22,.40,BLUE),
          text(2.24,5.23,3.17,.32,'Datamodellerat lager',14.5,INK,True),
          line(3.52,5.82,3.52,6.09,BLUE),
          icon('chart-bar',2.16,6.14,.35,BLUE),
          text(2.64,6.15,2.45,.30,'Rapportering och BI',14,INK,True)]
    for x,ico,label in [(7.23,'database','IT-stöd'),(8.92,'broadcast','Köer'),
                         (10.61,'file-text','Loggar')]:
        o += [shape(x,2.98,1.63,.67,WHITE,'CDE8E1'),
              icon(ico,x+.11,3.10,.38,TURQUOISE),
              text(x+.57,3.16,1.04,.29,label,14,INK,True)]
    o += [line(9.80,3.68,9.80,4.02,TURQUOISE),
          shape(7.28,4.08,5.00,.83,'D2EEE7','A8DAD0'),
          icon('archive',7.52,4.28,.42,TURQUOISE),
          text(8.08,4.21,3.80,.32,'Lagring & tabellformat',14.5,INK,True),
          text(8.08,4.58,3.91,.29,'Metadata · kvalitet · behörigheter',14,MUTED),
          line(8.41,4.93,8.41,5.30,TURQUOISE),
          line(11.17,4.93,11.17,5.30,TURQUOISE),
          shape(7.23,5.37,2.32,.74,WHITE,'CDE8E1'),
          icon('chart-bar',7.46,5.55,.39,TURQUOISE),
          text(8.02,5.57,1.36,.30,'BI & SQL',14,INK,True),
          shape(10.16,5.37,2.32,.74,WHITE,'CDE8E1'),
          icon('brain',10.38,5.55,.39,TURQUOISE),
          text(10.94,5.57,1.35,.30,'Analys & AI',14,INK,True),
          text(7.47,6.32,4.79,.31,'Samma data, flera användningar',14,INK,True,'center')]
    o+=footer('Skillnaden handlar om arkitekturella möjligheter – inte om att slopa governance eller datamodellering.')
    return {'objects':o}

def build_model():
    return {'theme':'executive-clean','size':[W,H],
            'slides':[generations(),ai_transition(),data_architecture()]}

def classify_contrast_overlays(model,issues):
    """Recognize the false positive from conservative text-on-page contrast audit.

    Only intentional white text on an opaque, preceding colored shape is accepted.
    All other warnings remain blocking for the model; pixel inspection is separate.
    """
    from quality import contrast
    accepted=[]
    remaining=[]
    for item in issues:
        if item['code']!='contrast':
            remaining.append(item)
            continue
        objects=model['slides'][item['slide']]['objects']
        o=objects[item['path'][0]]
        def covers(bg,fg):
            return (bg['type']=='shape' and bg.get('fill') not in (None,'none')
                and bg.get('fill_opacity',1)==1 and
                bg['x'] <= fg['x'] and bg['y'] <= fg['y'] and
                bg['x']+bg['w'] >= fg['x']+fg['w'] and
                bg['y']+bg['h'] >= fg['y']+fg['h'])
        backgrounds=[x for x in objects[:item['path'][0]] if covers(x,o)]
        if o.get('color')=='FFFFFF' and backgrounds and contrast('FFFFFF',backgrounds[-1]['fill'])>=4.5:
            accepted.append({'slide':item['slide']+1,'label':o['text'],
                             'actual_contrast':round(contrast('FFFFFF',backgrounds[-1]['fill']),2)})
        else: remaining.append(item)
    return accepted,remaining


def verify_pdf_text_placement(pptx, output):
    """Catch font-substitution wrapping that the model-level audit cannot see."""
    import subprocess
    import tempfile
    import xml.etree.ElementTree as ET
    with tempfile.TemporaryDirectory() as temp:
        d=Path(temp)
        profile=(d/'profile').as_uri()
        subprocess.run(['libreoffice','-env:UserInstallation='+profile,'--headless',
                        '--convert-to','pdf','--outdir',str(d),str(pptx.resolve())],
                       capture_output=True,check=True,timeout=90)
        pdf=d/(pptx.stem+'.pdf')
        assert pdf.exists(), 'LibreOffice did not produce PDF'
        bbox=d/'text-bbox.html'
        subprocess.run(['pdftotext','-bbox',str(pdf),str(bbox)],
                       capture_output=True,check=True,timeout=30)
        root=ET.parse(bbox).getroot()
        pages=root.findall('.//{*}page')
        assert len(pages)==3
        checks=[]
        for idx,(page,start,end) in enumerate(zip(pages,
                   ('Från','Från','En'),('utveckling','arbetsflöden','analysmöjligheterna')),1):
            words=[w for w in page.findall('{*}word') if w.text]
            def first(label):
                hits=[w for w in words if w.text.strip('.,:')==label]
                if not hits: raise AssertionError(f'Slide {idx}: word {label!r} missing from actual rendered PDF')
                return min(hits,key=lambda w:float(w.get('yMin')))
            start_word=first(start)
            end_word=first(end)
            delta=abs(float(end_word.get('yMin'))-float(start_word.get('yMin')))
            assert delta<=6, f'Slide {idx}: heading wraps unexpectedly in PDF (line delta={delta:.1f} pt)'
            checks.append({'slide':idx,'heading_line_delta_pt':round(delta,2)})
        data=pages[2]
        words=[w for w in data.findall('{*}word') if w.text]
        def word(label):
            hits=[x for x in words if x.text.strip('.,:')==label]
            if not hits: raise AssertionError(f'Data slide: missing {label}')
            return min(hits,key=lambda x:float(x.get('yMin')))
        title_start=word('Lagring')
        title_end=word('tabellformat')
        metadata=word('Metadata')
        assert abs(float(title_start.get('yMin'))-float(title_end.get('yMin')))<=5, \
            'Lakehouse panel heading wraps unexpectedly'
        assert float(metadata.get('yMin')) > float(title_end.get('yMax'))+1, \
            'Lakehouse metadata overlaps heading in actual PDF'
    return checks

def produce(output,preview=False):
    output.mkdir(parents=True,exist_ok=True)
    model=build_model()
    issues=audit(model)
    accepted,unresolved=classify_contrast_overlays(model,issues)
    (output/'advanced-compositions.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n')
    pptx=output/'advanced-compositions.pptx'
    render(model,pptx)
    prs=Presentation(pptx)
    checks=[]
    for i,slide in enumerate(prs.slides,1):
        checks.append({'slide':i,'shapes':len(slide.shapes),
                       'editable_vector_shapes':len(list(slide._element.iter(qn('a:custGeom')))),
                       'raster_pictures':len(list(slide._element.iter(qn('p:pic')))),
                       'text_shapes':sum(bool(sh.has_text_frame and sh.text.strip()) for sh in slide.shapes)})
    result={'automated_warnings':issues,'contrast_overlays_checked':accepted,
            'unresolved_audit_warnings':unresolved,'slides':checks,
            'visual_review':'not_determined_by_automated_tests'}
    if preview:
        files=previews(pptx,output/'previews')
        from PIL import Image
        sheet=Image.new('RGB',(2200,1980),'white')
        for i,f in enumerate(files):
            with Image.open(f) as im:
                im=im.convert('RGB');im.thumbnail((2200,660));sheet.paste(im,(0,i*660))
        sheet.save(output/'contact-sheet.png')
        result['previews']=[str(f.relative_to(output)) for f in files]
        result['rendered_text_placement']=verify_pdf_text_placement(pptx,output)
    (output/'technical-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Slides:',len(prs.slides),'Warnings:',len(issues),
          'Approved text-on-dark overlays:',len(accepted),'Unresolved:',len(unresolved))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--with-previews',action='store_true')
    a=p.parse_args()
    produce(a.output_dir,a.with_previews)
