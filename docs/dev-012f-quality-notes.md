# DEV-012F – Kvalitetsgranskning och förankrade samband

## Bakgrund
DEV-012E visade att en presentationsmodell kan vara tekniskt korrekt och ändå få klippt text efter fontsubstitution i GitHub CI. Den tidigare `quality.audit` antog dessutom sidbakgrund bakom vanliga textobjekt och gav åtta falska kontrastvarningar när vit text placerades ovanpå mörka rubrikfält. Relationslinjer krävde manuellt uppdaterade koordinater.

## Implementerade förändringar

### 1. Kontrast enligt ritordning
- Modellgranskaren använder tema och sidbakgrund, sedan solida former som helt täcker textens bounding box, i faktisk ordning.
- Halvtransparenta solida fyllningar kompositeras mot bakomliggande färger. **Flera lager** stöds.
- Gradienter, partiellt täckande former och ofullständigt kända bakgrunder ger `contrast_unknown`. Resultatet kräver rendering och manuell inspektion; det får **inte** klassas som godkänt.
- `correct(model)` ändrar inte originalet och försöker bara korrigera **faktiskt** låg kontrast med känd bakgrund. Den gissar inte för gruppbarn eller okänd bakgrund.
- DEV-012E:s specialundantag för vit text på färgade band tas bort. Den generella granskaren förväntas klara samma bilder utan undantag.

### 2. Textmått med läsbarhetsgräns
- `estimate_text_lines(text, width_pt, size_pt)` uppskattar word-wrap med ordgränser och variation mellan smala och breda tecken.
- `suggest_text_size(text, width_in, height_in, preferred_pt, min_pt=14, padding_in=0)` ger ett **förslag**, inte en garanti om faktisk rendering. Rutan måste förstoras eller texten kortas om inget läsbart alternativ ryms. Inga tysta krympningar under 14 punkter.
- Textpassningsgranskningen använder den ordmedvetna uppskattningen. För komplexa presentationer krävs fortfarande faktisk PNG/PDF-rendering och granskning av textplacering.

### 3. Dynamiskt förankrade relationer
Exempel i `examples/anchored-connections.yaml`:

```yaml
- {type: shape, id: source, x: 1, y: 2, w: 2, h: 1}
- {type: shape, id: target, x: 5, y: 2, w: 2, h: 1}
- type: line
  from_id: source
  to_id: target
  from_side: right
  to_side: left
  arrow: true
```

- `from_id` och `to_id` refererar till unika, positionerade objekt på samma sida.
- Tillåtna ankarpunkter: `left`, `right`, `top`, `bottom`, `center`; standard är right/left.
- Ändpunkter löses från komponenternas aktuella geometri före varje rendering; det spelar ingen roll om linjen deklareras före komponenterna.
- Grupper och `transform_objects` stöds, och källmodellen muteras inte. Dubbeldefinitioner, saknade ID:n, fel kantnamn samt blandning av `from/to` med `from_id/to_id` ger tydliga fel.
- Relationslinjer är fortsatt redigerbara PowerPoint-kopplingar. De är inte automatiskt ortogonala eller hinderundvikande; mer avancerad dragning kan vara framtida arbete.

## Regressionsbevis och öppna begränsningar
- `tests/test_quality_layout.py` täcker korrekta och felaktiga färger, halvtransparens, gradienter, partiell täckning, textmått, ankarpositioner, grupper, transformeringar och ogiltiga samband.
- `tests/test_advanced_compositions.py` kräver nu ren generell audit för de tre DEV-012E-bilderna.
- De tidigare DEV-012D-bildernas textboxar justerades för att inte spänna över två olika zoner (liten geometrisk justering i JSON-källan).
- `examples/anchored-connections.yaml` renderas av GitHub CI till redigerbar PPTX och PNG, publicerad som artefakten `anchored-connections-preview`.
- **Teknisk CI är en egen grind.** Visuell acceptans i Microsoft PowerPoint och de tidigare kvarstående funktionella värdtester är fortfarande separata kontroller.

## Nästa beslut
Efter CI och granskning av den nya exempelbilden: gå vidare med DEV-013 (releasekandidat) först när kvaliteten bedöms tillräcklig för praktiska arkitekturbilder. Annars avgränsa nästa förbättring efter ett påvisat renderingsfel; återinför inte ett bibliotek av fasta figurer.
