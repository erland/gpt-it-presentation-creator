# Utvecklingsplan

1. **Projektgrund** – Kanonisk profil, tre Skills, status och fem validerade paket.
2. **Designsystem** – Tre stilar med färgroller, typografi, avstånd och exempelbilder.
3. **Figurbibliotek** – 20–30 generiska IT-figurer, presentationskomponenter och metaforer med licensinformation.
4. **Visualiseringsbibliotek** – Fem flexibla layouter; före–efter, lager, generationer, förmågekarta, informationsflöde.
5. **PowerPoint-motor** – Redigerbara former, text och samband; separat Engine ZIP och verkligt självtest.
6. **Visuell kvalitetskontroll** – Rendera, inspektera och korrigera; kontrollera klippning, kontrast och överlapp.
7. **Befintliga presentationer** – Bevara original; granska och skapa reviderad PPTX.
8. **Acceptanstester** – Testa fyra IT-generationer, AI-förflyttning och plattformsarkitektur; bedöm visuell kvalitet och redigerbarhet.
9. **Release** – Lint, tester, runtimekontroller, hygiene och kompletta ZIP-paket.
10. **DEV-010** – Obligatorisk Engine-preflight, versionslänk, invänta uppladdning och uttryckligt godkänd fallback. Verifiera alla fem distributioner och värdbeteende.
11. **DEV-011** – Konsolidera till en Skill med progressiv inläsning, bevara beteende och verifiera fem runtimepaket.

**DEV-008B (komplettering till steg 8):** avancerad grafisk rekonstruktion, genomförd lokalt i 0.8.1.

DEV-008C: lokalt regressionstest för komplexa kompositioner.

DEV-008D – grafisk förädling, lokalt verifierad; värdtester återstår.

DEV-008F: grafisk komposition och obligatorisk visuell acceptansgrind; värdtester och oberoende användaracceptans återstår.

DEV-008E: professionella originalikoner och native SVG. DEV-009: releasekandidat; stabil release först efter värdacceptans.

DEV-009B: GitHub CI och manuell taggbaserad release, lokalt verifierade.

12. **DEV-012A** – Tekniskt ikonbibliotek och semantiskt register; verifiera native-konvertering och distributionsparitet. DEV-012B–D följer med avveckling av egna figurer, grafiska byggblock och visuell acceptans.

**DEV-012A2** – Visuell konsolidering av 195 definitioner; dokumentera urval och ersättningar före DEV-012B.

**DEV-012B** – Avveckla de 30 egna figurerna och migrera exempel och tester till fria kompositioner. Behåll 127 professionella ikoner.

**DEV-012C** – Ingen ny katalog med sammansatta figurer: komplettera Engine med redigerbara zoner, transparenta paneler och heldragna/streckade flöden. Verifiera ny exempelarkitektur och regressionstester. **DEV-012D** – Visuell renderingsgranskning av typiska arkitekturillustrationer samt oberoende värdacceptans.

**DEV-012D – genomfört under separat granskningssteg:** fyra leverantörsneutrala referensarkitekturer i fri JSON-baserad kompositionsmodell; deterministisk PPTX-generering, tekniska regressionstester, faktiska LibreOffice/PNG-renderingar och tre dokumenterade visuella granskningsomgångar. Se `docs/visual-review-012d.md`. Full CI, oberoende visuell kontroll av CI-artefakterna och funktionell värdacceptans krävs för slutligt godkännande.

**DEV-012E – avancerad kompositionsacceptans:** tre fördjupade prov (fyra IT-generationer, verksamhetsintegrerad AI, DW → Lakehouse) med redigerbara PPTX, faktisk PNG-rendering, tre visuella granskningsomgångar, regressionskontroller och specificerade begränsningar. Se `docs/visual-review-012e.md`. **DEV-012F** avgränsas till verkliga fel i bakgrundsmedveten kontrastanalys, textpassning, förankrade samband och kompositionskvalitet. GitHub CI och värdacceptans ska verifieras separat.
