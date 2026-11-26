"""Render a freely composed YAML deck into editable PowerPoint objects."""
import argparse, math, copy
from pathlib import Path
from figures import THEMES, rgb, KINDS
import yaml
from vector import gradient, path
from svg_native import draw_svg
from figures import ROOT
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.oxml.ns import qn
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.xmlchemy import OxmlElement


def transform_objects(objects, scale, dx=0, dy=0):
    """Uniformly transform a reusable composition, including text and strokes."""
    if not math.isfinite(scale) or scale <= 0: raise ValueError('Invalid scale')
    result=copy.deepcopy(objects)
    for o in result:
        if o['type']=='group': o['children']=transform_objects(o['children'],scale,dx,dy)
        elif o['type']=='line':
            for key in ('from','to'):
                if key in o:o[key]=[o[key][0]*scale+dx,o[key][1]*scale+dy]
        else:
            o['x']=o['x']*scale+dx;o['y']=o['y']*scale+dy
            for key in ('w','h'): o[key]*=scale
        for key in ('size','stroke_pt','padding'):
            if key in o:o[key]*=scale
    return result

def resolve_anchored_lines(objects):
    """Return a copy where semantic connections target actual component edges.

    This is evaluated on every render; IDs must be unique within the slide.
    Existing coordinate lines and source models remain unchanged.
    """
    index={}
    def collect(nodes):
        for o in nodes:
            if o['type']=='group':
                collect(o['children'])
            elif o.get('id') and o['type']!='line':
                key=o['id']
                if key in index:raise ValueError(f'Duplicate anchor id: {key}')
                try: x,y,w,h=(float(o[k]) for k in ('x','y','w','h'))
                except (KeyError,TypeError):raise ValueError(f'Anchor lacks bounds: {key}')
                if not all(map(math.isfinite,(x,y,w,h))) or w<=0 or h<=0:
                    raise ValueError(f'Invalid anchor bounds: {key}')
                index[key]=(x,y,w,h)
    collect(objects)
    def point(name,side):
        if name not in index:raise ValueError(f'Unknown connection anchor: {name}')
        x,y,w,h=index[name]
        offsets={'left':(0,.5),'right':(1,.5),'top':(.5,0),
                 'bottom':(.5,1),'center':(.5,.5)}
        if side not in offsets:raise ValueError(f'Unknown anchor side: {side}')
        a,b=offsets[side]
        return [x+a*w,y+b*h]
    result=copy.deepcopy(objects)
    def bind(nodes):
        for o in nodes:
            if o['type']=='group':
                bind(o['children'])
            elif o['type']=='line' and ('from_id' in o or 'to_id' in o):
                if not o.get('from_id') or not o.get('to_id'):
                    raise ValueError('Anchored line requires both from_id and to_id')
                if 'from' in o or 'to' in o:
                    raise ValueError('Anchored line cannot also specify raw coordinates')
                o['from']=point(o['from_id'],o.get('from_side','right'))
                o['to']=point(o['to_id'],o.get('to_side','left'))
    bind(result)
    return result

def render(model, output, assets=Path('.')):
    r=Presentation(); W,H=model.get('size',[13.333,7.5]); r.slide_width=Inches(W);r.slide_height=Inches(H)
    def color(v,t): return rgb(t.get(v,v))
    def bounds(o):
        a=[float(o[k]) for k in ('x','y','w','h')]
        x,y,w,h=a
        if not all(map(math.isfinite,a)) or min(x,y)<0 or min(w,h)<=0 or x+w>W+.001 or y+h>H+.001: raise ValueError(f'Invalid bounds: {o}')
        return a
    dash_styles={'solid':MSO_LINE_DASH_STYLE.SOLID,'dash':MSO_LINE_DASH_STYLE.DASH,'dot':MSO_LINE_DASH_STYLE.ROUND_DOT}
    def dash(line, o):
        style=o.get('stroke_dash','solid')
        if style not in dash_styles: raise ValueError(f'Unknown stroke_dash: {style}')
        if style != 'solid': line.dash_style=dash_styles[style]
    def opacity(shape, o):
        if 'fill_opacity' not in o: return
        value=o['fill_opacity']
        if not isinstance(value,(float,int)) or not math.isfinite(value) or not 0<=value<=1:
            raise ValueError('fill_opacity must be between 0 and 1')
        if o.get('fill') == 'none' or 'gradient' in o:
            raise ValueError('fill_opacity requires a solid fill')
        solid=shape.fill._xPr.find(qn('a:solidFill'))
        color_node=solid.find(qn('a:srgbClr'))
        alpha=OxmlElement('a:alpha'); alpha.set('val',str(round(value*100000)));color_node.append(alpha)
    def add(shapes,o,t):
        k=o['type']
        if k=='group':
            g=shapes.add_group_shape()
            for child in o['children']: add(g.shapes,child,t)
            s=g
        elif k=='line':
            a=o['from'];b=o['to']
            if any(not (0<=p[0]<=W and 0<=p[1]<=H) for p in (a,b)): raise ValueError('Line outside slide')
            s=shapes.add_connector(MSO_CONNECTOR.STRAIGHT,*map(Inches,[*a,*b]));s.line.color.rgb=color(o.get('color','accent'),t);s.line.width=Pt(o.get('stroke_pt',2));dash(s.line,o)
            style=s._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
            if style is not None:s._element.remove(style)
            for end in (['headEnd','tailEnd'] if o.get('arrow')=='both' else ['tailEnd'] if o.get('arrow') else []):
                e=OxmlElement('a:'+end);e.set('type','triangle');s.line._get_or_add_ln().append(e)
        else:
            x,y,w,h=bounds(o); box=list(map(Inches,[x,y,w,h]))
            if k=='path':
                s=path(shapes,o['points'],x,y,w,h,color(o['stroke'],t) if o.get('stroke') else None,color(o['fill'],t) if o.get('fill') else None,o.get('stroke_pt',1.4),o.get('closed',False))
            elif k=='professional-icon':
                spec=yaml.safe_load((ROOT/'knowledge/figures/professional-icons.yaml').read_text())['icons'][o['icon']]
                s=draw_svg(shapes,spec['svg'],x,y,w,h,color(o.get('color','text'),t))
            elif k=='image':
                p=(assets/o['path']).resolve()
                if not p.is_relative_to(assets.resolve()): raise ValueError('Asset escapes root')
                if p.suffix.lower()=='.svg':
                    import cairosvg,io
                    p=io.BytesIO(cairosvg.svg2png(url=str(p),output_width=max(1,int(w*180)),output_height=max(1,int(h*180))))
                s=shapes.add_picture(p,*box)
            elif k in ('text','shape'):
                s=shapes.add_textbox(*box) if k=='text' else shapes.add_shape(KINDS[o.get('shape','rect')],*box)
                if k=='shape':
                    if o.get('fill') == 'none': s.fill.background()
                    else: s.fill.solid();s.fill.fore_color.rgb=color(o.get('fill','surface'),t)
                    s.line.fill.background()
                    if 'stroke' in o:
                        s.line.color.rgb=color(o['stroke'],t);s.line.width=Pt(o.get('stroke_pt',.7));dash(s.line,o)
                    elif 'stroke_dash' in o:raise ValueError('stroke_dash requires stroke')
                    if 'gradient' in o:
                        if o.get('fill') == 'none':raise ValueError('gradient requires fill')
                        gradient(s,[color(c,t) for c in o['gradient']],o.get('gradient_angle',0))
                    opacity(s,o)
                    if o.get('shape')=='round':s.adjustments[0]=o.get('roundness',.12)
                    style=s._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
                    if style is not None:s._element.remove(style)
                if 'text' in o:
                    f=s.text_frame;f.clear();f.word_wrap=True;f.margin_left=f.margin_right=f.margin_top=f.margin_bottom=Inches(o.get('padding',0));f.vertical_anchor=MSO_ANCHOR.MIDDLE if o.get('valign')=='middle' else MSO_ANCHOR.TOP
                    for i,line in enumerate(o['text'].split('\n')):
                        p=f.paragraphs[0] if i==0 else f.add_paragraph();p.text=line;p.space_before=Pt(0);p.space_after=Pt(0);p.font.name=o.get('font','Aptos');p.font.size=Pt(o.get('size',20));p.font.bold=o.get('bold',False);p.font.color.rgb=color(o.get('color','text'),t);p.alignment={'left':PP_ALIGN.LEFT,'center':PP_ALIGN.CENTER,'right':PP_ALIGN.RIGHT}[o.get('align','left')]
            else: raise ValueError(f'Unknown object type {k}')
        if 'id' in o:s.name=o['id']
    def recalc(shapes):
        for shape in shapes:
            if hasattr(shape,'shapes'):
                recalc(shape.shapes)
                shape._element.recalculate_extents()
    for slide in model['slides']:
        t=THEMES[slide.get('theme',model.get('theme','executive-clean'))];s=r.slides.add_slide(r.slide_layouts[6]);s.background.fill.solid();s.background.fill.fore_color.rgb=color(slide.get('background','background'),t)
        for o in resolve_anchored_lines(slide['objects']):add(s.shapes,o,t)
        recalc(s.shapes)
    r.save(output)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('model',type=Path);p.add_argument('output',type=Path);a=p.parse_args();render(yaml.safe_load(a.model.read_text()),a.output,a.model.parent)
