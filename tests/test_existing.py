import sys, tempfile, zipfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/itpc'))
from existing import inspect,revise
from pptx import Presentation
from pptx.util import Inches
class ExistingTest(unittest.TestCase):
 def test_selective(self):
  with tempfile.TemporaryDirectory() as d:
   a,b=Path(d)/'a.pptx',Path(d)/'b.pptx'; p=Presentation();s=p.slides.add_slide(p.slide_layouts[6]);o=s.shapes.add_textbox(Inches(1),Inches(1),Inches(3),Inches(1));o.text='Test';p.slides.add_slide(p.slide_layouts[6]);p.save(a);original=a.read_bytes();revise(a,b,[{'slide':1,'id':o.shape_id,'box':[2,1,3,1],'font_size':24}]);self.assertEqual(a.read_bytes(),original);self.assertEqual(inspect(b)['slides'][0]['shapes'][0]['text'],'Test')
   with zipfile.ZipFile(a) as x,zipfile.ZipFile(b) as y:self.assertEqual([n for n in x.namelist() if x.read(n)!=y.read(n)],['ppt/slides/slide1.xml'])
   with self.assertRaises(ValueError):revise(a,a,[])
if __name__=='__main__':unittest.main()
