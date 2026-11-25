# IT Presentation Creator
Version 0.5.3 (planerad) – releasekandidat; värdacceptans återstår. GitHub-baserad utveckling. Läs PROJECT.md, STATUS.md och docs/development-plan.md. Fem runtimepaket byggs från canonical/. Egen PPTX-motor ingår som separat Engine-paket. Alternativ filgenerering kräver uttryckligt godkännande enligt DEV-010.

## Designsystem 0.2.0
Se knowledge/design/ och examples/design-styles.pptx. Exempelgeneratorn är utvecklingsverktyg, inte runtimeverktyg. Kör python tests/test_design.py med python-pptx och PyYAML.

## Figurbibliotek 0.3.0
Se knowledge/figures/ för 127 professionella ikoner. Katalogen genereras vid behov. Generera katalogen med python examples/generate_catalog.py. Kör pytest tests för samtliga tester.

## Visualiseringsbibliotek 0.5.0
Tio kompositioner i fem familjer, tre teman. Se knowledge/visualizations/ och examples/visualization-catalog.pptx. Generera med python examples/generate_visualizations.py.

DEV-005: generell PowerPoint-motor, se knowledge/engine-guide.md.

DEV-008B: rekonstruktion av referensbild, se examples/reconstruction.pptx och knowledge/reconstruction-guide.md.

DEV-008E: 73 originalikoner, native SVG-kurvor, lokal rendering; värdtester återstår.

DEV-008F: obligatorisk visuell acceptansgrind och reproducerbar komposition i examples/compose_generations.py.

GitHub-projekt: se [CI och release](docs/github-release.md).

DEV-011: en sammanhållen Skill med tre progressivt inlästa arbetsflöden under knowledge/workflows/. Kritiska grindar ligger kvar i canonical/core.md.
