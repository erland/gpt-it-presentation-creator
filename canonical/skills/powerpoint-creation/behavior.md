# powerpoint-creation

Använd 16:9 som standard. Skapa konsekvent typografi, marginaler och färgroller. Gruppera relaterade objekt när verktyget stödjer det. Använd generiska IT-symboler och visuella metaforer; undvik onödiga rutor. Använd värdens PPTX-funktioner; använd figurbiblioteket i knowledge/figures/library.yaml med färgroller från themes.yaml; använd den generella motorn enligt knowledge/engine-guide.md. Skapa fri YAML-komposition, kör självtest och exportera PPTX. Om motorn inte är åtkomlig, be om matchande Engine ZIP eller använd värdens PPTX-funktioner och redovisa avvikelsen. Kontrollera att filen öppnas och att centrala objekt är redigerbara.

Följ quality-guide.md: rendera, inspektera varje sida, korrigera modellen och rendera igen. Rapportera tekniska och visuella kontroller separat; påstå aldrig att visuell granskning utförts utan bildinspektion.

Vid rekonstruktion från referensbild: följ reconstruction-guide.md, använd redigerbara konturikoner och fria vektorformer, rendera och jämför med originalet.

För komplexa arkitekturkompositioner: återanvänd grupper och skala dem proportionellt med transform_objects; använd arrow: both för dubbelriktade samband. Bevara referensens innehåll och färgsemantik. Rendera översikt och detaljbilder.

Använd professional-icon för originalikoner enligt professional-icons-guide.md; behåll licensinformation vid distribution.

Obligatorisk visuell acceptansgrind: följ visual-acceptance.md. Granska varje faktiskt renderad sida; komplexa illustrationer kräver minst två dokumenterade granskningsomgångar. Redovisa teknisk och visuell status separat. Utan faktisk bildinspektion är visuell status ej verifierad; vid väsentliga kvarstående brister leverera endast som utkast.

Prioritera Phosphor Regular för tekniska symboler, Bold för små symboler och Fill för avsiktliga silhuetter; Tabler är komplement. Välj en sammanhängande familj per komposition. Egna sammansatta figurer används när de förmedlar IT-struktur bättre. Kontrollera faktiska ikon-ID:n i biblioteket. Vid uttryckligt krav på redigerbarhet använd native vektorformer, inte rasteriserade SVG eller referensbild som bakgrund. Om matchande Engine eller rendering saknas, redovisa begränsningen och be om paketet vid behov; påstå inte att motorn körts. Bevara tredjepartslicenser vid vidareförmedling av ikonresurser.
