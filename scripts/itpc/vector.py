from pptx.util import Inches, Pt
from pptx.oxml.xmlchemy import OxmlElement
from pptx.enum.shapes import MSO_SHAPE
from figures import rgb

def no_style(s):
    style=s._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
    if style is not None:s._element.remove(style)

def gradient(shape, stops, angle=0):
    shape.fill.gradient(); shape.fill.gradient_angle=angle
    g=shape.fill.gradient_stops
    if len(stops)!=2: raise ValueError('Two gradient stops required')
    for s,c in zip(g,stops): s.color.rgb=c

def path(shapes, points, x,y,w,h, stroke, fill=None, width=1.4, closed=False):
    if len(points)<2 or any(not 0<=v<=100 for p in points for v in p): raise ValueError('Invalid normalized path')
    coords=[(int(Inches(x+w*a/100)),int(Inches(y+h*b/100))) for a,b in points]
    f=shapes.build_freeform(*coords[0]);f.add_line_segments(coords[1:],close=closed);s=f.convert_to_shape()
    if fill:s.fill.solid();s.fill.fore_color.rgb=rgb(fill)
    else:s.fill.background()
    if stroke:s.line.color.rgb=rgb(stroke);s.line.width=Pt(width)
    else:s.line.fill.background()
    no_style(s)
    return s

def icon(shapes, spec, x,y,w,h,c, stroke_scale=1):
    g=shapes.add_group_shape()
    def tint(f):
        return "".join(f"{round(v+(255-v)*f) if f>=0 else round(v*(1+f)):02X}" for v in rgb(c))
    for kind, data in spec:
        width=1.4*stroke_scale
        if kind.endswith('path'):
            fills={'solid-path':rgb(c),'light-path':tint(.65),'dark-path':tint(-.22)}
            fill=fills.get(kind)
            path(g.shapes,data,x,y,w,h, 'FFFFFF' if kind=='white-path' else c if fill is None else None,fill, width*(2 if kind=='white-path' else 1),closed=fill is not None)
        else:
            a,b,d,e=data;s=g.shapes.add_shape(MSO_SHAPE.OVAL if kind.endswith('oval') else MSO_SHAPE.ROUNDED_RECTANGLE,*map(Inches,[x+w*a/100,y+h*b/100,w*d/100,h*e/100]))
            if kind in ('solid-oval','white-oval'):
                s.fill.solid();s.fill.fore_color.rgb=rgb('FFFFFF' if kind=='white-oval' else c);s.line.fill.background()
            else:
                s.fill.background();s.line.color.rgb=rgb(c);s.line.width=Pt(width)
            no_style(s)
    return g
