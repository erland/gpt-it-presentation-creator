# GitHub CI och release

Planerat repository: erland/gpt-it-presentation-creator. ZIP är fortsatt leveransform.

1. Packa upp projekt-ZIP och checka in hela projektet inklusive `.github`.
2. Kontrollera CI i Actions (push, PR eller manuell start).
3. Skapa och pusha en tagg, exempelvis `v1.0.0-rc.2`, på verifierad commit.
4. Actions → Build release distributions → Run workflow → ange taggen.
5. Granska draft-release med sju ZIP, SHA256SUMS.txt och DELIVERY-MANIFEST.json. Publicera manuellt när godkänd. Befintlig publicerad release skrivs inte över.

CI och release använder GPT Byggaren 1.6.33:s kanoniska mallar, anpassade till fem runtime-mål, separat Engine, projektets beroenden och manuell taggtrigger. Byggaren är oförändrad. Källvalidatorn körs före bygge; efter bygge körs kanonisk distributionsvalidator samt check_release_assets.py, eftersom den generella leveransvalidatorn räknar Engine som ett extra runtimepaket.

GitHub Actions har inte exekverats på GitHub ännu. Lokala kommandon har verifierats. Visuell acceptans kräver fortfarande mänsklig/AI-granskning och de fyra värdtesterna.
