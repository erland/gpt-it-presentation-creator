import unittest,yaml
from pathlib import Path
from pptx import Presentation
ROOT=Path(__file__).resolve().parents[1]
def lum(c):
 v=[int(c[i:i+2],16)/255 for i in (0,2,4)];return sum(w*(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4) for w,x in zip((.2126,.7152,.0722),v))
class Design(unittest.TestCase):
 def test_contrast(self):
  for t in yaml.safe_load((ROOT/'knowledge/design/themes.yaml').read_text())['themes'].values():
   for a,b in [('text','background'),('text','surface'),('muted','background'),('on_primary','primary')]:
    x,y=sorted([lum(t[a]),lum(t[b])]);self.assertGreaterEqual((y+.05)/(x+.05),4.5)
 def test_deck(self):
  r=Presentation(ROOT/'examples/design-styles.pptx');self.assertEqual(len(r.slides),3)
  for s in r.slides:
   self.assertGreater(len(s.shapes),10)
   for a in s.shapes:
    self.assertGreaterEqual(a.left,0);self.assertGreaterEqual(a.top,0);self.assertLessEqual(a.left+a.width,r.slide_width);self.assertLessEqual(a.top+a.height,r.slide_height)
if __name__=='__main__':unittest.main()
