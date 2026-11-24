# Verifiering 0.1.0
Motor 1.6.33: manifesthashar och kanoniskt självtest godkända. Kanonisk lint godkänd. Fem distributioner och projekt-ZIP validerade. Hygiene: endast genererade build/dist-kataloger, exkluderade ur projekt-ZIP. Skill-schemat i motorn saknar resource_policy trots att leveransvalidatorn kräver fältet; projektunik schemautvidgning tillåter explicit/inferred utan att ändra motorn. Stateful-validatorn kördes men kräver explicit state machine; inte ett godkänt test för guided. Funktionella värdtester och PPTX-motor återstår.

## 0.2.0
Kanonisk lint: PASS (0 fel, 0 varningar), hygiene PASS före bygge. Två deterministiska tester: kontrast och objektgränser, PASS. Tre PPTX-sidor renderade i LibreOffice och visuellt inspekterade; standardformernas skuggor avlägsnade och omrenderade. Inga uppenbara klippningar. Värdtester och egen motor återstår.

## 0.3.0
Fyra pytest-tester godkända (inklusive bibliotekets koordinater, färgroller, komponentreferenser, gruppobjekt och 87 figurinstanser). 15 katalogsidor renderade med LibreOffice och inspekterade som kontaktkarta. Kanonisk lint och hygiene godkända. Värdtester återstår.

## DEV-004
Tio kompositioner i tre teman. 30 sidor renderade med LibreOffice och visuellt inspekterade i kontaktkarta. Tester kontrollerar referenser, redigerbara grupper och sidgränser. Ingen generell runtime-motor ännu.

## DEV-006
8 pytest-tester och motorsjälvtest godkända. Två slides renderade före och efter kontrastkorrigering; slutbilder inspekterade, pilskugga avlägsnad. Inga synliga klippningar. Heuristiska kontroller har begränsningar enligt quality-guide.md. Värdtester återstår.

## DEV-008
Tre scenarier, två bilder vardera, renderade före och efter justering. Första granskningen: komponentgenerationen illustrerades missvisande med en ensam applikation; breda figurer sträcktes. Ny sammansatt komponentfigur och valfri contain-passning införda. 10 pytest-tester godkända; samtliga sex modellerade bilder utan audit-anmärkningar. Visuell bedömning är lokal, inte oberoende användaracceptans. Illustrationerna är fortfarande schematiska. Värdtester återstår.

DEV-008B: 11 pytest godkända; en referensbild renderad två gånger och visuellt granskad. Native gradienter, fria former och 20 konturikoner. Små texter är avsiktliga för referenslikhet; värdtester återstår.

DEV-009: källarkivens SHA-256, licenstexter och samtliga 73 SVG-definitioner jämförda mot originalarkiven. Värdtester är inte utförda. Separat Engine valideras utanför de fem runtimepaketen.

DEV-009B: 16 pytest, kanonisk lint/hygiene/källvalidering, CI-versionens sju arkiv, distributionsvalidering och uppackad Engine verifierade lokalt. GitHub-host och visuell användaracceptans återstår.
