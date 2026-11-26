# DEV-012E – Avancerade grafiska kompositioner och acceptans

## Syfte

Stresstesta om IT Presentation Creator kan skapa mer komplexa bilder med **fri komposition och 127 professionella originalikoner**, utan att återinföra låsta arkitekturfigurer. Tre betydligt mer informationsrika scenarier än DEV-012D används som regressionsprov.

## Tre testscenarier

| Bild | Komposition | Innehåll | Native redigerbara vektorformer | Totalt top-level-objekt |
|---|---|---|---:|---:|
| 1 | Fyra generationspaneler med olika intern arkitektur | Monolit; tjänster och API:er; plattformssjälvservice; verksamhet med AI | 13 | 68 |
| 2 | Asymmetrisk före-/efterjämförelse med intern orkestrering och tre funktionella resurser | Separat AI-tjänst kontra användare → agent → språkmodell/IT-stöd/specialiserad AI, inklusive MCP, kontroller och logg | 8 | 53 |
| 3 | Två dataplattformsmönster med olika informationsflöden | ETL → DW → BI kontra delad datagrund med flera datakällor och analys-/AI-konsumenter | 12 | 55 |

Leverans: `examples/advanced_compositions.py` genererar en 3-sidig PPTX, individuella PNG-renderingar, kontaktkarta, exakt JSON-modell och `technical-review.json`.

## Dokumenterade renderings- och granskningsomgångar

**Omgång 1: första PPTX/LibreOffice-rendering.** Manuell genomgång av alla tre PNG-bilder och maskinell modellgranskning. 65 varningar: flera under 14 pt, två- eller fler-radiga etiketter i för små textrutor samt kontrastvarningar för vit text på färgade paneler. I de faktiskt renderade bilderna syntes klippt/korsande text på flera platser, särskilt i AI-bildens högra resurskolumn och inom generationspanelerna.

**Omgång 2: korrigering och ny rendering.** Komponentnamn kortades, antalet ord i metadata minskades, minsta teckenstorlek höjdes och AI-resursernas kort breddades genom att arbetsflödesdelen fördelades om. Antalet modellvarningar sjönk från 65 till 13. Även efter andra renderingens bildinspektion återstod en överspänd rubrik för medarbetarprocessen samt för lång etikett i kontrollpanelen.

**Omgång 3: slutlig korrigering, rendering och bildinspektion.** Namnet blev `Medarbetare`, undertexten `Mål och beslut` och kontrollpanelens text `MCP · skydd · logg`. Gen 3 har en kortare självserviceetikett och dataexemplet har kompakta, läsbara källnamn. **Ingen varning om textpassning eller för liten text återstår i den konservativa audit-körningen.** De tre PNG-bilderna kontrollerades åter i helhet.

## Särskild iakttagelse: kontrastkontrollens falska positiva

Slutmodellen har exakt åtta **kontrastvarningar** från dagens `quality.audit` eftersom verktyget beräknar kontrast mot sidans bakgrund för text på en separat form. Samtliga åtta avser avsiktlig **vit rubriktext ovanpå en heltäckande mörk panel**.

Vi har därför lagt till en *separat, explicerbar kontroll* för dessa åtta fall. Den accepterar endast text med `FFFFFF` som geometriskt täcks av en tidigare ritad, ogenomskinlig form vars faktiska färg ger minst 4,5:1 kontrast. Andra auditvarningar godkänns inte. Korrigeringsbehovet ska hanteras i DEV-012F: bakgrundsmedveten kontrastanalys i huvudgranskaren.

## Teknisk status

- **Lokal rendering:** 3 PPTX-sidor, 3 PNG-förhandsvisningar och kontaktkarta genererade.
- **Redigerbarhet:** 13, 8 respektive 12 native custom geometries; inga rasterbilder.
- **Model audit:** 0 kvarvarande varningar efter riktad, verifierbar klassificering av åtta falska positiva. Den ursprungliga `audit`-utskriften är bevarad i `technical-review.json`; varningar har inte tystats.
- **Visuell lokal granskning:** renderad och manuellt granskad tre gånger. Ingen väsentlig klippning eller oavsiktlig radbrytning kvarstod i sista versionen.
- **GitHub CI och Microsoft PowerPoint:** separata grindar. GitHub ska rendera om samma källkod och publicera `advanced-composition-previews`. Oberoende acceptans i PowerPoint är ännu inte genomförd.

## Begränsningar och nästa förbättringar – DEV-012F

1. **Text över färgade former.** Den befintliga kvalitetsgranskningen tar inte hänsyn till underliggande fyllning och ger åtta falska varningar. Inför bakgrundsmedveten kontrastkontroll utan att undanta verkliga kontrastfel.
2. **Textpassning.** Långa svenska IT-begrepp krävde flera manuella förkortningar. Förbättra textmått, layoutval och varningsrapport i stället för att sänka teckenstorleken.
3. **Relationer och rörliga kompositioner.** Motorn använder koordinatbaserade linjer; automatisk förankring mot komponentkanter och mer uttrycksfulla, villkorade samband saknas.
4. **Visuellt uttryck.** Bildexemplen är mer innehållsrika, men fortfarande delvis panel- och kortbaserade. Kommande förbättringar bör prioritera friare komposition, grafiska metaforer och högkvalitativa detaljer – **inte** ett nytt bibliotek med låsta figurer.
5. **Oberoende PowerPoint-test.** Redigerbarhet verifieras med DrawingML/python-pptx och LibreOffice, men slutlig Microsoft PowerPoint-beteendeacceptans återstår.

**Beslut:** DEV-012E är ett jämförande acceptanstest och en konkret prioriterad förbättringslista, inte ett bevis på att alla avancerade arkitekturbilder redan uppnår slutlig produktionskvalitet. Gå vidare till DEV-012F först utifrån verkliga brister i genererade bilder.
