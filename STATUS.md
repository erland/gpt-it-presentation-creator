# Status
DEV-011 inför 0.5.3: en Skill, tre interna arbetsflöden och oförändrad Engine. CI och praktisk värdacceptans återstår. 0.5.2 är distribuerad enligt användarens bifogade paket; DEV-010:s värdbeteende behöver fortfarande testas.

DEV-012A: 54 nya Phosphor Regular-ikoner och 63 registrerade tekniska begrepp. CI och visuell acceptans återstår.

DEV-012A2: katalog renderad och urvalspolicy införd; CI återstår. 38 äldre konturikoner borttagna; 157 aktiva definitioner.

DEV-012B: 30 egna figurer och typen figure avvecklade; 127 professionella ikoner kvar. CI godkänd: 23 tester, Engine-självtest och sju distributionspaket. DEV-012C: fria byggblock för zoner, halvtransparent fyllning och heldragna/streckade samband med regressionstester tillagda. Slutlig CI godkänd för commit aa3ecd78: 32 tester, självtest, projekthygien, alla sju distributioner och paritetskontroll. Visuell acceptans återstår till DEV-012D.

DEV-012B: även de tre incheckade YAML-acceptansexemplen migrerade från avvecklad figurtyp till professionella redigerbara ikoner. De inkluderades i den godkända CI-körningen.

DEV-012D: fyra redigerbara, leverantörsneutrala arkitekturreferenser (hybrid, händelser, datagrund, AI) har skapats och granskats i tre lokala LibreOffice-renderingsomgångar; sista lokala modellen hade 0 automatiska audit-avvikelser, inga rasterbilder och konsekvent flödessemantik. `examples/reference-architectures.json`, renderare, tester, CI-artefakt och granskningsrapport har lagts till på utvecklingsgrenen. GitHub CI för själva PR:en och oberoende värdacceptans återstår.

DEV-012E: tre mer komplexa redigerbara kompositioner med varierade layouter har genererats, renderats och visuellt granskats i tre omgångar. Lokal bildgranskning efter korrigering: 0 textpassningsvarningar, 0 varningar om för liten text, 8 klassificerade kontrastvarningar (vit text på mörka band) som inte undantagits generellt. CI-grind och användarens PowerPoint-acceptans återstår. Utifrån faktiska brister föreslås DEV-012F: bättre textmått, bakgrundsmedveten kontrast och mer flexibel layout.

DEV-012F (på PR): ny generell bakgrundsmedveten kontrastanalys utan specialundantag, ordmedveten textpassningsanalys och minst 14 punkter vid textstorleksförslag, ID-förankrade relationslinjer och nya negativa regressionstester. Slutlig CI och PowerPoint-värdacceptans återstår.

DEV-013 (PR under arbete): Efter mergad DEV-012F förbereds releasekandidat `0.5.3-rc.1`. CI ska bygga sju ZIP, verifiera version, Engine-identitet, ikonparitet, SHA256 och faktiska referensrenderingar. Ingen tagg, publicerad prerelease eller stabil release skapas av PR-arbetet. DEV-010/011-värdtester och praktisk PowerPoint-acceptans återstår.
