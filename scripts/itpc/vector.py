from pptx.util import Inches, Pt
from pptx.oxml.xmlchemy import OxmlElement
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
