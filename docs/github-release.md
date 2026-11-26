# GitHub CI och release

Repository: erland/gpt-it-presentation-creator.

## DEV-013: kandidat 0.5.3-rc.1

1. Kontrollera att CI är godkänd för exakt commit. Artefakten `release-candidate-0.5.3-rc.1` innehåller sju ZIP, kontrollsummor, leveransmanifest och separat verifieringsrapport; den är **inte** en publicerad release.
2. Granska `docs/dev-013-release-candidate.md` och `docs/release-tests.md`.
3. Först efter godkänd PR och kandidatverifiering: skapa taggen `v0.5.3-rc.1` på den verifierade committen.
4. Använd Actions → Build release distributions → Run workflow → den **befintliga taggen**. Om releasen saknas skapar arbetsflödet ett **utkast** och laddar upp kontrollerade filer.
5. Verifiera tagg, commit, samtliga sju ZIP, SHA256SUMS.txt, DELIVERY-MANIFEST.json och Actions-rapporten `release-candidate-verification`.
6. Utför praktiska värdtester. Publicera eventuell kandidat som **prerelease** först efter beslut. Stabil release kräver separat användaracceptans.

## Viktiga begränsningar

- En GitHub Actions-artefakt är inte samma sak som en publicerad Release. En versionsspecifik nedladdningslänk får inte beskrivas som tillgänglig innan den fungerar.
- `release: published` startar distributionsbygget, men publicering ersätter inte kvalitetsgrindarna. För en draft-kandidat använd manuell `workflow_dispatch`.
- Vid befintligt assetnamn laddar flödet ned den befintliga filen och kräver byteidentiskt innehåll. Identiska filer återanvänds utan överskrivning; avvikande innehåll stoppar publiceringskörningen. Saknade filer laddas upp. En delvis genomförd uppladdning kan därmed återköras säkert, men testade paket ska aldrig bytas ut under samma versionsnummer.
- Test i Microsoft PowerPoint samt verklig installation i valda värdar sker separat; vid fel dokumentera avvikelsen och skapa nästa kandidat.

Projektet använder GPT Byggaren 1.6.33:s kanoniska mallar för fem runtimepaket och separat Engine. Releaseflödet kör lint, test, projekthygien, Engine-självtest, verklig PPTX/PNG-rendering, distributionsbygge och kandidatverifiering innan uppladdning.

Den senast publicerade versionen före DEV-013 är `0.5.2`; `0.5.3-rc.1` är föreslagen, inte publicerad.
