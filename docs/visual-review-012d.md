# DEV-012D – Visuell referensgranskning av fria arkitekturkompositioner

## Omfattning

Fyra konceptuella, leverantörsneutrala arkitekturillustrationer granskas som **redigerbara PowerPoint-kompositioner**, inte som nya fasta figurer i biblioteket:

1. **Hybrid/cloud native:** eget datacenter och alternativ driftsmiljö, automatiserad leverans och likvärdiga plattformsförmågor. Portabilitet anges uttryckligen som arkitekturmål, inte som automatisk garanti.
2. **Händelsedriven integration:** publicerande IT-stöd, händelseplattform och prenumererande konsumenter. Streckade flöden markerar asynkron händelseförmedling; kontrakt och felhantering framgår i fotnoten.
3. **Data och analys:** källdata, gemensam datagrund med metadata och tabellformat samt flera konsumenter. Lakehouse presenteras som ett möjligt arkitekturmönster, inte som enda lösning.
4. **AI-assistent/agent:** användare, orkestrering, behörighet, loggning, sökning, språkmodell, IT-stöd och separat kunskapsindex. Läsa/ändra sker under behörighetskontroll.

Kanonisk presentationsmodell: `examples/reference-architectures.json`. Den använder endast `professional-icon`, `shape`, `text` och `line`. Inga rasterbilder, inga `type: figure` eller återinförda sammansatta katalogfigurer. Alla ikoner väljs från Phosphor Regular.

## Faktiska visuella granskningsomgångar

**Omgång 1 – renderad med LibreOffice Impress och inspekterad i PNG**

- Bild 1: arkitekturbudskapet och två driftszoner framgår, men portabilitetspilen behöver fortsatt tydlig förankring som princip snarare än garanti.
- Bild 2: `Transaktionssystem`, prenumerantzonens rubrik och plattformens etikett bröts olyckligt eller trängdes ihop. Åtgärd: kortare kortetiketter, tydligare zonrubrik och omskriven plattformsetikett.
- Bild 3: kortet för händelser och filer fick klippt/radbrytande rubrik. Åtgärd: kortare namn och förtydligad dataundertext.
- Bild 4: rubriken för anslutna tjänster bröts, samtidigt som kunskapssökning saknade separat källa. Åtgärd: kortare zonrubrik och separat kunskapsindex.

**Omgång 2 – omrendering och ny bildinspektion**

- Oavsiktliga radbrytningar i de större rubrikerna är borta.
- Förbättrade titlar och ökad undertextstorlek gav i några små kort ytterligare radbrytningar.
- Åtgärd: förenkla korttexterna, höj stödtext till minst 14 punkter, tillåt avsedda överlapp genom `allow_overlap` på dekorativa paneler och ikoner, separera synkrona och asynkrona linjers betydelse.
- Uppföljningskontroll fann två kvarvarande uppskattade `text_fit`-varningar.

**Omgång 3 – slutlig omrendering och visuell inspektion**

- Korttexten för IT-stöd i datavyn förenklades till `Tabeller`.
- Etiketten för datagrunden fick större texthöjd.
- Modelltjänstens förklarande text förenklades till `Genererar text`.
- Ospecificerade dataflöden respektive modell-/systemanrop visas heldragna. Endast asynkron händelseförmedling använder streckad linje.
- Alla fyra bilder inspekterades i fullbreddsrendering. Ingen väsentlig klippning eller oavsiktlig radbrytning kvarstod vid denna granskning.

Den slutliga lokala modellerade presentationen hade **0 resultat från den konservativa automatiska modellgranskningen**. Den granskningen ersätter inte faktisk bildinspektion.

## Teknisk granskning

Följande har verifierats på den lokalt renderade modellen med motsvarande motorfunktioner och ursprungliga ikonformer:

| Bild | Redigerbara objekt på högsta nivån | Native custom geometry | Rasterbilder | Streckade element | Halvtransparenta fyllningar |
|---|---:|---:|---:|---:|---:|
| Hybrid/cloud native | 36 | 6 | 0 | 0 | 2 |
| Händelsedriven integration | 36 | 5 | 0 | 4 | 3 |
| Data & analys | 34 | 5 | 0 | 0 | 3 |
| AI-assistent/agent | 39 | 7 | 0 | 0 | 3 |

De fullständiga PowerPoint- och renderingskontrollerna upprepas i GitHub Actions mot **aktuell kanonisk källkod** genom `examples/render_reference_architectures.py` och `tests/test_reference_architectures.py`. CI laddar upp `reference-architecture-previews` med `reference-architectures.pptx`, fyra faktiska PNG-renderingar, en kontaktkarta och `technical-review.json`. Kontrollera dessa bildartefakter innan en release kallas visuellt accepterad.

## Bedömning och begränsningar

**Teknisk bedömning av den lokala modellen:** Godkänd. Alla fyra sidor kan skapas som öppningsbar, redigerbar PowerPoint med native vektorformer, text och samband, utan rasterbaserade ikoner.

**Visuell bedömning av lokala LibreOffice-renderingar:** Godkänd för illustrationsbibliotekets konceptuella referensbruk efter tre dokumenterade granskningsomgångar. Bilderna är medvetet förenklade; de ska inte betraktas som fullständiga lösningsarkitekturer eller formell notation. En stor uppskalad arkitekturbild med många komponenter behöver fortfarande särskild renderingsgranskning.

**Kvarstår:** Oberoende granskning av GitHub Actions-renderingarna och funktionella tester i användarens presentationsvärdar, inklusive Microsoft PowerPoint. Validerad teknisk redigerbarhet i python-pptx är inte samma sak som full användaracceptans.

**Nästa beslut:** Bedöm om kvaliteten i dessa fyra referenser räcker som startnivå eller om fler variationsrika kompositionsprover behövs före stabil release.
