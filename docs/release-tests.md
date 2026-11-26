# Praktisk acceptans – 0.5.3-rc.1
Installera det verifierade pluginpaketet för exakt kandidatversion. Starta en ny chatt per test, välj pluginen och bifoga Engine ZIP **0.5.3-rc.1** om värden inte redan har en verifierat matchande Engine. Kontrollera version, Engine-manifest, SHA256 och självtest; vid saknat eller ogiltigt paket måste assistenten efterfråga rätt Engine utan automatisk fallback. Ändra inte pluginen under testet. Spara PPTX, renderingar och granskningsrapport. Godkänn varje test separat efter egen inspektion i PowerPoint. Rapportera teknisk och visuell status samt värd, datum och avvikelser.

## 1. Rekonstruktion (bifoga en tidigare oanvänd referensbild)
Återskapa bifogad IT-illustration som en redigerbar PowerPoint-bild. Bevara innehåll, proportioner och visuell hierarki. Använd en alternativ harmonisk färgpalett. Använd inte originalbilden som bakgrund. Rendera, jämför och korrigera i minst två dokumenterade granskningsomgångar. Leverera PPTX, PNG och separat teknisk och visuell bedömning.

## 2. Fri komposition (ingen referensbild)
Skapa en redigerbar svensk PowerPoint-bild för IT-ledningen som visar förflyttningen från punkt-till-punkt-integration till händelsedriven integration. Visa kopplingar i nuläget, publicering och prenumeration via en händelseplattform i målbilden, nyttor och nya krav på styrning, övervakning och felhantering. Använd en fri grafisk komposition med enhetliga ikoner, inte en texttung punktlista. Rendera, granska och korrigera. Leverera PPTX och PNG.

## 3. Komplett presentation (ingen referensbild)
Skapa sju svenska 16:9-bilder för en myndighets IT-ledning om övergången från beställningsbaserad IT-drift till plattformsbaserad självservice. Visa nuläge, målbild, ansvarsfördelning, plattformsförmågor, införande, risker och beslutspunkter. Variera kompositionen men behåll grafisk profil. Hitta inte på siffror. Rendera och granska varje sida; leverera redigerbar PPTX och granskningsrapport.

## 4. Befintlig presentation (bifoga en PPTX)
Granska bifogad presentation och förbättra selektivt typografi, placering, kontrast och grafisk balans. Bevara fakta, befintlig grafisk profil och originalfil. Ändra inte sidor som redan fungerar. Leverera en separat redigerbar PPTX, renderade före/efter-bilder för ändrade sidor och en ändringslogg. Redovisa eventuella objekt som inte kunde bevaras.

## Godkännandekriterier
- Alla fyra: verklig öppningsbar PPTX, inga väsentliga klippningar eller oavsiktliga överlapp, konsekvent bildspråk, dokumenterad faktisk rendering och bildinspektion.
- Test 1: hög visuell likhet och redigerbara centrala objekt; test 2: korrekt begripligt flöde; test 3: sju varierade sammanhängande bilder; test 4: originalets hash oförändrad och profil/fakta bevarade.
- Underkänd eller ej verifierad visuell status blockerar stabil release. Ingen kodändring under testen; vid fel dokumentera och skapa ny kandidat.

## DEV-013: kompletterande värd- och versionsacceptans

- Verifiera separat att Chat ZIP, Claude Project, Claude Skills, OpenCode och OpenAI Plugin exponerar obligatorisk Engine-preflight och ett konsekvent Skill-beteende **i verklig värdmiljö**; CI-paritet räcker inte.
- I nytt projekt: testa att saknad Engine leder till versionsspecifik länk och avbrott, inte automatisk alternativ generering. Bifoga sedan matchande ZIP och verifiera självtest före faktisk PPTX-generering.
- Öppna levererad PPTX i Microsoft PowerPoint, redigera text, flytta en ikon, spara och öppna på nytt. OBS: ID-förankrade linjer omberäknas av Engine **vid generering**, inte automatiskt när ett objekt dras manuellt i PowerPoint.
- För komplicerade bilder: minst två dokumenterade visuella granskningsomgångar. Kontrollera verklig rendering och native vektorobjekt där redigerbarhet krävs.
- Registrera per test: värd, versionsnummer, Engine-hash, datum, indata, PPTX, PNG, resultat, avvikelse och faktisk godkännare. Sätt status **inte genomfört** tills testet körts.
