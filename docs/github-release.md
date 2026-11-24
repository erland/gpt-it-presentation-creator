# GitHub CI och release

Repository: erland/gpt-it-presentation-creator. GitHub är leveransform.

1. Kontrollera CI på main.
2. Skapa och publicera en GitHub Release med en tagg (exempelvis v1.0.0-rc.3) på verifierad commit.
3. Publicering startar Build release distributions automatiskt, även för prerelease.
4. Kontrollera Actions och releasens sju ZIP, SHA256SUMS.txt och DELIVERY-MANIFEST.json.

Manuell start: Actions → Build release distributions → Run workflow → ange befintlig tagg. Om release saknas skapas ett utkast. Befintliga publicerade releaser kan kompletteras; om något av de avsedda filnamnen redan finns avbryts uppladdningen utan överskrivning. Vid delvis uppladdning måste operatören granska befintliga filer före nytt försök.

CI och release använder GPT Byggaren 1.6.33:s kanoniska mallar, anpassade till fem runtime-mål och separat Engine. Byggaren är oförändrad. Källvalidatorn körs före bygge; efter bygge körs kanonisk distributionsvalidator samt check_release_assets.py.

Första GitHub CI är godkänd (45340557157). Det uppdaterade releaseflödet och fyra praktiska värdtester återstår att verifiera.
