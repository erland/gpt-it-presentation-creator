# Figurbibliotek
25 grundfigurer och metaforer samt fyra sammansatta illustrationer. Originalgrafik skapad för projektet, utan externa ikonpaket; får återanvändas i genererade presentationer. Ingen tredjepartslicens krävs för dessa former.

`library.yaml` beskriver varje figur med stabilt ID, svensk etikett, kategori, delar och valfria komponenter. Koordinater är relativa till 100 × 100. Delar anges som [form, x, y, bredd, höjd, färgroll]; för line är bredd/höjd signerade ändpunktsförskjutningar. Komponenter anges som [figur-ID, x, y, bredd, höjd]. Rita delar i ordning, sedan komponenter rekursivt. Använd samma färgroller från themes.yaml; behåll proportioner och gruppera figuren. Textetiketter ligger separat. Former kan anpassas och förenklas efter budskap; använd inte katalogen som obligatorisk notation. Vid behov av mer avancerade illustrationer, använd värdens bildfunktioner.

Katalogen i projektets examples/ visar alla figurer i alla tre stilar. Generera den med `python examples/generate_catalog.py` (python-pptx och PyYAML). Detta är ett utvecklingsverktyg, inte ett obligatoriskt runtimeverktyg. Den egna generella PowerPoint-motorn kommer i DEV-005.

Konturikonerna inkluderar cloud native (cube, container, api, events, infinity, scale, wrench, cloud), team-workstation, person-solid, check-status och warning-status. Se examples/generations.py i projektet för återanvändbara plattforms- och infrastrukturkompositioner.

DEV-008D: välj `team-filled`, `person-filled`, `check-filled`, `warning-filled` eller `cube-faceted` för fyllda och fasetterade symboler. Tidigare konturer finns kvar. `stroke_scale` styr ikonens linjebredd och följer transform_objects. Använd små hörnradier på stora paneler, starka rubriker och konsekventa färgroller. Jämför renderingen med referensen; teknisk likhet räcker inte.
