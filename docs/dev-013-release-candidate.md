# DEV-013 – Releasekandidat 0.5.3-rc.1

**Status:** kandidatbyggning och verifiering i GitHub CI. Detta dokument är inte ett protokoll över godkänd värdacceptans eller en publicerad GitHub Release.

## Omfattning

Kandidaten samlar samtliga mergade förbättringar från DEV-011 och DEV-012A–F:
- en gemensam Skill med tre progressivt inlästa arbetsflöden;
- 127 professionella SVG-ikoner i native PowerPoint-format och konsekvent register;
- fria arkitekturkompositioner med transparenta zoner och separata informationsflöden;
- bakgrundsmedveten kontrast, ordmedveten textgranskning och ID-förankrade samband;
- obligatorisk Engine-preflight utan implicit fallback och redigerbar PowerPoint.

## Versionsstrategi

- **Föreslagen version:** `0.5.3-rc.1`. Den senast publicerade versionen är `0.5.2`.
- **Föreslagen tagg:** `v0.5.3-rc.1`, men skapa inte tagg eller publicerad release före godkännande av PR och kandidatgrind.
- `0.5.3-rc.1` är **inte** `1.0.0`, och betyder inte att alla värdtester är klara.
- Releaseinstruktioner får inte peka på en förmodat publicerad kandidatlänk innan GitHub-artefakterna faktiskt finns. Värdtester som förutsätter en GitHub-releaselänk kräver kandidatens draft/prerelease eller motsvarande verifierad installationskälla.

## Verifiering – tre separata nivåer

| Nivå | Bevis | Godkännandekrav |
|---|---|---|
| 1. Källkod och test | GitHub Actions på aktuell PR-head | Lint, hela pytest-sviten, hygien, Engine-självtest, fyra + tre + en renderade referensbilder |
| 2. Paket och releasekandidat | `scripts/verify_release_candidate.py` + `scripts/check_release_assets.py` | Sju ZIP, fem runtime-versioner, Engine-version, SHA256, ingen dold versionsavvikelse, exakt ikonparitet |
| 3. Värd- och användaracceptans | Separat utfört testprotokoll i `docs/release-tests.md` | Installation, Engine-preflight, faktisk PowerPoint-redigerbarhet, grafisk kvalitet och fyra scenariospecifika tester |

**OBS:** Nivå 1 och 2 kan passera automatiskt. Nivå 3 får inte markeras godkänd enbart utifrån CI eller LibreOffice.

## Paketen som ska verifieras

Exakt sju ZIP-arkiv med samma versionssträng:
1. `it-presentation-creator-project-0.5.3-rc.1.zip`
2. `it-presentation-creator-chat-0.5.3-rc.1.zip`
3. `it-presentation-creator-claude-project-0.5.3-rc.1.zip`
4. `it-presentation-creator-claude-skills-0.5.3-rc.1.zip`
5. `it-presentation-creator-opencode-0.5.3-rc.1.zip`
6. `it-presentation-creator-plugin-0.5.3-rc.1.zip`
7. `it-presentation-creator-engine-0.5.3-rc.1.zip`

Därtill `SHA256SUMS.txt`, `DELIVERY-MANIFEST.json` och separat `verification.json`.

## Föreslaget genomförande efter godkänd PR

1. Kontrollera att CI på exakt kandidatcommit är grön och hämta `release-candidate-0.5.3-rc.1` från Actions. Verifiera ZIP, manifest och Engine-hashar.
2. Skapa en tagg `v0.5.3-rc.1` **på den verifierade merge-committen på `main`**, inte godtyckligt på en senare commit.
3. Använd manuella `Build release distributions` med den existerande taggen så att ett **releaseutkast** kan skapas. Detta är separerat från publicering. Kontrollera att alla filer hamnar på utkastet. Vid en senare publicering körs releaseflödet igen: befintliga assets återanvänds endast om de är byteidentiska med de nybyggda paketen, annars avbryts körningen utan överskrivning.
4. Utför praktiska värdtester mot exakt samma kandidatpaket, se `docs/release-tests.md`.
5. Dokumentera eventuella fel. Vid fel skapa **en ny** kandidat (t.ex. `0.5.3-rc.2`) utan att tyst byta ut en kandidat som redan testats.
6. Publicera bara en **prerelease** efter beslut. Den stabila versionen är blockerad tills separat faktisk användaracceptans är godkänd.

## Kvarstående hinder och risker

- **DEV-010:** verklig värdpreflight behöver testas med matchande Engine; fallback får inte aktiveras automatiskt.
- **DEV-011:** instruktionerna i alla värdar ska testas praktiskt, inte enbart som byteidentiska filer.
- **Funktionell redigerbarhet:** kontrollera förflyttning, redigering och sparning i riktig Microsoft PowerPoint.
- **Visuell användaracceptans:** särskilt rekonstruktion av okänt motiv och en sammanhållen presentation med varierad grafisk komposition.
- **Releaseflöde:** tagg och draft-prerelease ska granskas innan publicering; `release: published`-triggern publicerar inga kvalitetsgarantier i sig.

**Nästa beslut:** Är `0.5.3-rc.1` redo att installeras för värdacceptans? Svaret kräver verifierad CI och granskad kandidatpaketlista. Det är inte samma fråga som om versionen är redo för stabil produktion.
