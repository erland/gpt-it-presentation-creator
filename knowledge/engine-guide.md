# PowerPoint Engine
Packa upp matchande Engine ZIP, verifiera manifestets SHA-256 och kör `python scripts/itpc/selftest.py`. Python kräver python-pptx, PyYAML fonttools och (för rasteriserad SVG) CairoSVG. Kör `python scripts/itpc/render.py deck.yaml output.pptx`. Se demo.yaml i Engine. Modellen har theme, size (tum), slides med objects i ritordning. Varje slide kan välja theme och background. Objekt: text, shape, image, line, group, professional-icon, path. Text/shape/image använder x,y,w,h i tum. Text: text,size (pt),bold,color,align,valign,padding,font. Shape: shape (rect,round,oval,can,cloud,hex,pentagon,callout,gear,fold,trapezoid,arrow),fill,stroke och valfri text. Line: from,to (koordinatpar),color,stroke_pt,arrow. Group: children med absoluta slide-koordinater. Image: path relativt modellfilens katalog; SVG rasteriseras, bilder är flyttbara men inte vektorredigerbara. Färger är temaroller eller sexsiffrig RGB. Valfritt id blir objektnamn. Mönsterbiblioteket är designreferens, inte en låst mallmotor. Kontrollera rendering och textpassning separat; gränskontroll garanterar inte frånvaro av överlapp eller klippning.

Figurobjekt kan ange `fit: contain` för att centrera en kvadratisk biblioteksfigur utan att sträcka den. Utelämnat fit behåller tidigare beteende.

DEV-008B: native gradienter, normaliserade fria polygoner och grupperade professionella ikoner. Se reconstruction-guide.md.

## Återanvändbara kompositioner
`transform_objects(objects, scale, dx, dy)` skalar och förflyttar nästlade objekt, textstorlek och explicita linjebredder utan att mutera originalet. Koordinater är i tum. `arrow: both` ger pilspetsar i båda ändar. Skapa en komposition en gång och använd samma modell för översikt och detaljbild.

Använd professional-icon för originalikoner enligt professional-icons-guide.md; behåll licensinformation vid distribution.

## DEV-010
Följ kärnans obligatoriska Engine-preflight. Vid saknad eller ogiltig motor: ge exakt versionslänk och invänta uppladdning; alternativ exekvering endast efter uttryckligt godkännande. Ren rådgivning kräver ingen motor.
