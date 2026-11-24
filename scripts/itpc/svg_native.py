"""Native DrawingML conversion for a restricted, monochrome SVG icon subset."""
from xml.etree import ElementTree as ET
from fontTools.svgLib.path import parse_path
from fontTools.pens.basePen import BasePen
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.xmlchemy import OxmlElement
from figures import rgb
from vector import no_style
import math

class Pen(BasePen):
    def __init__(self, path, view): super().__init__(None); self.path=path; self.view=view
    def emit(self, tag, *pts):
        e=OxmlElement('a:'+tag)
        for x,y in pts:
            p=OxmlElement('a:pt');p.set('x',str(round((x-self.view[0])/self.view[2]*100000)));p.set('y',str(round((y-self.view[1])/self.view[3]*100000)));e.append(p)
        self.path.append(e)
    def _moveTo(self,p): self.emit('moveTo',p)
    def _lineTo(self,p): self.emit('lnTo',p)
    def _curveToOne(self,*p): self.emit('cubicBezTo',*p)
    def _qCurveToOne(self,*p): self.emit('quadBezTo',*p)
    def _closePath(self): self.emit('close')
    def _endPath(self): pass

def draw_svg(shapes, data, x,y,w,h,color):
    root=ET.fromstring(data); view=list(map(float,root.attrib['viewBox'].split())); assert len(view)==4 and min(view[2:])>0
    ratio=min(w/view[2],h/view[3]); ww,hh=view[2]*ratio,view[3]*ratio;x+=(w-ww)/2;y+=(h-hh)/2
    g=shapes.add_group_shape()
    def visit(el, inherited):
        a={**inherited,**el.attrib}; tag=el.tag.split('}')[-1]
        if any(k in el.attrib for k in ('transform','style','clip-path','mask','opacity','fill-opacity','stroke-opacity')): raise ValueError('Unsupported SVG styling')
        if tag in ('svg','g'):
            for child in el:visit(child,a)
            return
        if tag=='path':d=el.attrib['d']
        elif tag=='circle':
            cx,cy,r=[float(a[k]) for k in ('cx','cy','r')];d=f'M{cx-r} {cy} a{r} {r} 0 1 0 {2*r} 0 a{r} {r} 0 1 0 {-2*r} 0 Z'
        elif tag=='line':d=f"M{a['x1']} {a['y1']} L{a['x2']} {a['y2']}"
        elif tag in ('polyline','polygon'):d='M'+a['points']+(' Z' if tag=='polygon' else '')
        elif tag=='rect':
            xx,yy,dx,dy=[float(a.get(k,0)) for k in ('x','y','width','height')];r=min(float(a.get('rx',0)),dx/2,dy/2);d=f'M{xx+r} {yy} H{xx+dx-r} Q{xx+dx} {yy} {xx+dx} {yy+r} V{yy+dy-r} Q{xx+dx} {yy+dy} {xx+dx-r} {yy+dy} H{xx+r} Q{xx} {yy+dy} {xx} {yy+dy-r} V{yy+r} Q{xx} {yy} {xx+r} {yy} Z'
        else:raise ValueError('Unsupported SVG element: '+tag)
        fill=a.get('fill','black');stroke=a.get('stroke','none')
        if a.get('fill-rule','nonzero')!='nonzero':raise ValueError('Unsupported fill rule')
        s=g.shapes.add_shape(MSO_SHAPE.RECTANGLE,*map(Inches,[x,y,ww,hh]));sp=s._element.spPr;sp.remove(sp.prstGeom)
        geom=OxmlElement('a:custGeom');sp.insert(1,geom)
        for k in ('avLst','gdLst','ahLst','cxnLst'):geom.append(OxmlElement('a:'+k))
        rect=OxmlElement('a:rect');rect.attrib.update({'l':'l','t':'t','r':'r','b':'b'});geom.append(rect)
        pl=OxmlElement('a:pathLst');geom.append(pl);p=OxmlElement('a:path');p.attrib.update({'w':'100000','h':'100000','fill':'none' if fill=='none' else 'norm','stroke':'0' if stroke=='none' else '1'});pl.append(p);parse_path(d,Pen(p,view))
        if fill=='none':s.fill.background()
        else:s.fill.solid();s.fill.fore_color.rgb=rgb(color)
        if stroke=='none':s.line.fill.background()
        else:
            s.line.color.rgb=rgb(color);s.line.width=Pt(float(a.get('stroke-width',1))*ratio*72);ln=s.line._get_or_add_ln();ln.set('cap','rnd');ln.append(OxmlElement('a:round'))
        no_style(s)
    visit(root,{})
    return g
