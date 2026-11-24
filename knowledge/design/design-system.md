# Designsystem 0.2
Välj Executive Clean som standard, Modern Technology för tekniska framtidsbilder, Editorial Professional för förklarande berättelser. Använd samma tema genom en presentation om inte ett avsiktligt avsnittsbyte motiverar annat. Använd tokens i themes.yaml (hex RGB). Accent är markering, inte automatiskt textfärg. Använd text på bakgrund och yta, on_primary på primary; kontrollera andra kombinationer (minst 4,5:1 för vanlig text, 3:1 för stor text). Färg får inte vara enda betydelsebärare.

## Komposition
16:9, 13,333 × 7,5 tum. Marginal 0,55 tum, mellanrum 0,24 tum, bassteg 0,08 tum. Rubrik 32–38 pt, underrubrik 18–22, brödtext 18–22, etikett 14–16, fotnot 11–12. Aptos med Arial som reserv. Undvik att krympa text för att få plats: dela hellre sidan. Vänsterställ löptext. Använd högst två typsnitt och tre textvikter. Skapa tydlig blickpunkt, sekundär information och luft. Använd linjer sparsamt, med konsekvent tjocklek 1–2 pt. Undvik dekorativa skuggor och gradienter som standard.

## Visuell grammatik
Nuläge: neutral yta; målbild: primary eller accent med textetikett. Förmågor: grupperade byggblock; flöden: riktade linjer; människor: enkla symboler; plattform: sammanhängande bas. Använd inte färg för flera konkurrerande betydelser. Variera komposition: stor konceptillustration, asymmetrisk berättelse, jämförelse eller horisontell resa. Välj efter budskap, inte efter mall. Executive: stram grid, tunna linjer. Modern: mörk yta, ljusa accenter, tydlig fokalpunkt. Editorial: asymmetri, stora siffror och luft, varm neutral bakgrund.

## Kontroll före leverans
Kontrollera textklippning, kontrast, marginaler, avsiktliga överlapp, balans, konsekvens och redigerbarhet. Rendera när möjligt och granska varje sida. Exemplen är designreferenser, inte obligatoriska mallar. Anpassa efter kundens grafiska profil utan att ge avkall på läsbarhet.

## Acceptansförbättringar
Använd en illustration som faktiskt skiljer varje utvecklingsfas från nästa: flera samverkande applikationer för komponentarkitektur, inte en ensam applikationsikon. Bevara figurproportioner med `fit: contain` vid placering i rektangulära ytor. Använd större illustrationer hellre än fler dekorativa element. Granska varje bild i full storlek.

## Tät referensgrafik
Bevara referensens palett och proportioner när användaren efterfrågar rekonstruktion. Använd diskreta gradienter, enhetliga konturikoner, tunna avdelare och tydlig hierarki. Mindre text är ett medvetet undantag för informationsrika referensbilder, inte standard för föredrag.

### Grafisk förädling
Använd fyllda människor och statusmarkörer för tydlig silhuett; fasetterade kuber för tekniska komponenter. Kombinera med konturikoner för infrastruktur. Begränsa stora panelers hörnradie så att innehållsytan inte förloras. Granska visuellt vid både översikts- och detaljskala.

Följ visual-acceptance.md för obligatorisk visuell acceptans och kompositionsregler.

Prioritera Phosphor Regular för tekniska symboler, Bold för små symboler och Fill för avsiktliga silhuetter; Tabler är komplement. Välj en sammanhängande familj per komposition. Egna sammansatta figurer används när de förmedlar IT-struktur bättre. Kontrollera faktiska ikon-ID:n i biblioteket. Vid uttryckligt krav på redigerbarhet använd native vektorformer, inte rasteriserade SVG eller referensbild som bakgrund. Om matchande Engine eller rendering saknas, redovisa begränsningen och be om paketet vid behov; påstå inte att motorn körts. Bevara tredjepartslicenser vid vidareförmedling av ikonresurser.
