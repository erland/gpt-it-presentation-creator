# Grafiska byggblock och fri arkitekturkomposition (DEV-012C)

Skapa ingen separat katalog över färdiga arkitekturfigurer. Komponera varje presentation med **professionella ikoner**, redigerbar text, former, linjer, fria vektorbanor och grupper. De 127 originalikonerna är symbolförrådet; tekniska etiketter väljs från technical-icon-register.yaml.

## Byggblock

- **Zon och systemgräns:** `shape: rect` eller `shape: round` med `fill: none`, `stroke: accent`, `stroke_pt` och valfritt `stroke_dash: dash`. Lägg zongränsen *före* ikonerna i objektordningen så att den hamnar bakom dem. Placera zonrubriken som ett eget redigerbart textobjekt.
- **Plattformslager och panel:** rektangel/avrundad rektangel med temaroll `fill: surface` eller `fill: primary`. För diskret färgyta använd `fill_opacity` mellan 0 och 1 på en solid fill. Opaciteten gäller fyllningen, inte text eller kantlinje. `fill: none` ger helt transparent bakgrund.
- **Relation:** `type: line` med `from`, `to`, `color`, `stroke_pt`, `arrow: true` eller `arrow: both`. `stroke_dash: solid|dash|dot` gäller såväl linjer som kantlinjer. Använd genomgående enhetlig semantik, exempelvis heldragen linje för synkront anrop och streckad linje för asynkron förmedling; textetikett måste göra innebörden tydlig.
- **Enskild komponent:** `professional-icon` följd av kort textetikett. Använd samma ikonfamilj och ungefär samma symbolstorlek per vy; symbolen ersätter inte komponentnamn.
- **Återanvändbar delkomposition:** `group` med `children` i absoluta slide-koordinater. `transform_objects(objects, scale, dx, dy)` skalar och flyttar hela delkompositionen. Skapa inte nya hårdkodade figur-ID:n.
- **Fritt samband eller form:** `type: path` för egna redigerbara polygoner och kurvfria konturer; använd inte raster om redigerbarhet är krav.

**DEV-012F:** Se `examples/anchored-connections.yaml` för flyttbara komponenter med redigerbara linjer som refererar till unika objekt-ID:n. Använd `from_id`, `to_id` och valfria `from_side` och `to_side` i stället för manuella koordinater. Ogiltiga ID:n eller kantnamn stoppar rendering. Anslutningarna omberäknas vid varje rendering.

## Design och kontroll

Välj zoner bara när de har faktisk arkitekturell betydelse; markera inte slumpmässiga boxar som ”plattform”. Relationer skall ansluta till komponenternas kanter, inte löpa över etiketter. Undvik flera visuella linjestilar för samma betydelse. Använd temaroller för kontrast och låt färgsemantiken vara stabil mellan vyer.

Både `fill_opacity` och `stroke_dash` är valfria; befintliga figurer behåller tidigare standardutseende. Ogiltiga värden ska stoppa genereringen. `fill_opacity` tillåts inte tillsammans med `gradient` eller `fill: none`. Detta är presentationsbyggblock, inte ett formellt arkitekturnotationsspråk.

**Demonstration:** `examples/graphic-blocks.yaml` visar driftszon, molnzon, synkront API-anrop, asynkron händelseförmedling, transparent zongräns och tematonad plattformsyta. Kontrollera resultatet i faktisk PowerPoint-rendering innan en komplex illustration godkänns.

## DEV-012D: testade referenskompositioner

`examples/reference-architectures.json` demonstrerar fyra fria kompositioner: hybridmiljöer, händelsedriven integration, en gemensam datagrund och en AI-assistent med separat kunskapsindex. De är **exempel** för vidare anpassning, inte beställbara figurer i ikonbiblioteket. Generera med `python examples/render_reference_architectures.py --output-dir build/reference-review --with-previews`. Läs `docs/visual-review-012d.md` i projektpaketet för faktisk granskningshistorik och begränsningar.

## DEV-012E: mer komplexa referensbilder

Tre prövade, **ej fördefinierade** kompositioner genereras av `examples/advanced_compositions.py`. De demonstrerar fyra generationer, AI integrerad i verksamhetsflöden och Data Warehouse → Lakehouse. Koden är ett reproducerbart utvecklings- och acceptansprov, inte ett register över beställbara figurer. Se `docs/visual-review-012e.md` för granskning och öppna begränsningar.
