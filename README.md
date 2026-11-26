# IT Presentation Creator
Föreslagen releasekandidat 0.5.3-rc.1 (DEV-013) – ännu ej publicerad eller stabil; värdacceptans återstår. GitHub-baserad utveckling. Läs PROJECT.md, STATUS.md och docs/development-plan.md. Fem runtimepaket byggs från canonical/. Egen PPTX-motor ingår som separat Engine-paket. Alternativ filgenerering kräver uttryckligt godkännande enligt DEV-010.

## Designsystem 0.2.0
Se knowledge/design/ och examples/design-styles.pptx. Exempelgeneratorn är utvecklingsverktyg, inte runtimeverktyg. Kör python tests/test_design.py med python-pptx och PyYAML.

## Figurbibliotek 0.3.0
Se knowledge/figures/ för 127 professionella ikoner och knowledge/graphic-composition-guide.md för zoner, linjer, paneler och fria kompositioner. Katalogen genereras vid behov. Generera katalogen med python examples/generate_catalog.py. Kör pytest tests för samtliga tester.

## Visualiseringsbibliotek 0.5.0
Tio kompositioner i fem familjer, tre teman. Se knowledge/visualizations/ och examples/visualization-catalog.pptx. Generera med python examples/generate_visualizations.py.

DEV-005: generell PowerPoint-motor, se knowledge/engine-guide.md.

DEV-008B: rekonstruktion av referensbild, se examples/reconstruction.pptx och knowledge/reconstruction-guide.md.

DEV-008E: 73 originalikoner, native SVG-kurvor, lokal rendering; värdtester återstår.

DEV-008F: obligatorisk visuell acceptansgrind och reproducerbar komposition i examples/compose_generations.py.

GitHub-projekt: se [CI och release](docs/github-release.md).

DEV-011: en sammanhållen Skill med tre progressivt inlästa arbetsflöden under knowledge/workflows/. Kritiska grindar ligger kvar i canonical/core.md.

### DEV-012D: redigerbara arkitekturreferenser

Fyra granskningsbilder definieras i `examples/reference-architectures.json` och genereras med
`python examples/render_reference_architectures.py --output-dir build/reference-review --with-previews`.
Denna komposition innehåller inte något nytt fast figur-ID. GitHub CI laddar upp både redigerbar PPTX och fyra renderade PNG samt teknisk rapport som artefakten `reference-architecture-previews`. Se `docs/visual-review-012d.md` för tre visuella granskningsomgångar och öppna begränsningar.

### DEV-012E: avancerade kompositioner

`python examples/advanced_compositions.py --output-dir build/advanced-review --with-previews` skapar tre innehållsrika och redigerbara PowerPoint-bilder (IT-generationer, verksamhetsintegrerad AI och Data Warehouse → Lakehouse), PNG och teknisk granskningsrapport. Se `docs/visual-review-012e.md` för dokumenterade visuella omgångar, kända begränsningar och rekommenderade DEV-012F-åtgärder. CI publicerar artefakten `advanced-composition-previews`.

### DEV-012F: relationer som följer komponenter

Använd `from_id` och `to_id` på linjer för att koppla dem till unika objekt-ID:n, eller behåll explicita `from/to`-koordinater. Se `examples/anchored-connections.yaml` och `docs/dev-012f-quality-notes.md`. `quality.audit` tar hänsyn till solida bakomliggande färger och transparens, och `suggest_text_size` föreslår läsbar textstorlek (minst 14 pt). GitHub CI laddar upp en faktisk PPTX/PNG som `anchored-connections-preview`.

### DEV-013: kandidatverifiering

GitHub CI bygger `0.5.3-rc.1` som **testartefakt** och verifierar alla sju ZIP-paket, SHA256, fem runtimeversioner och separat Engine. Se `docs/dev-013-release-candidate.md` för releaseprocedur och återstående värdtester. `scripts/verify_release_candidate.py` tillämpar motsvarande kontroll vid den taggade releasen.
