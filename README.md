# Pregătim reușita — Concurs directori 2026

60 de simulări originale × 20 de itemi (1.200 de itemi), pentru pregătirea probei cognitive din 13 octombrie 2026.

- Structură: 7 itemi verbali, 7 numerici și 6 logici.
- 60 de minute, patru variante, un singur răspuns corect.
- 0,5 puncte/item; prag de promovare 6/10.
- Răspunsuri și termen de finalizare păstrate în browser.
- Revizuire înainte de finalizare; soluțiile apar după finalizare.
- Seria 21–40: dificultate mai mare. Seria 41–50: dificultate moderată.
- Pentru 41–50: opțiuni în ordine alfabetică românească, etichete a, b, c, d, punctuație finală; explicații pe pași, metode alternative și tabele de adevăr unde sunt relevante.

Simulările 41–50 sunt exerciții originale. Respectă structura publicată de minister, fără a pretinde identitate cu subiectele care vor fi administrate sau o dificultate etalonată psihometric. Subtipurile exacte și repartizarea lor în interiorul celor trei categorii nu sunt anunțate în informarea de structură.

Structura: https://www.edu.ro/press_rel_67_26_informare_probe_concurs_directori

Formele de interpretare a textelor, analogii, categorii comune și calcule din tabele sunt adaptate din exemplele publice de itemi din 2021, cu texte și date originale: https://www.edu.ro/sites/default/files/_fi%C8%99iere/Minister/2021/concursuri/concurs%20directori/Itemi%20exemple%20selectie%20directori.pdf

Materiale: Prof. dr. Maria-Magdalena Dorcioman.

## Verificare

```sh
python scripts/validate_content.py
node --check app.js
node scripts/test_app.cjs
```

Validatorul inițial recalculează primele 400 de întrebări. Controlul suplimentar verifică structura tuturor testelor, unicitatea enunțurilor și identificatorilor, apoi recalculează independent problemele numerice și logice noi din 41–50. Testul aplicației parcurge toate cele 1.200 de întrebări și verifică navigarea, punctarea, persistența, timerul, finalizarea și ascunderea explicațiilor înainte de finalizare.

Reproducerea seriei 41–50:

```sh
python scripts/generate_exam_41_50.py
```

Generatorul necesită Python și Node.js pentru ordonarea variantelor cu collation românească. Nu modifică testele anterioare sau manifestul.

## Publicare

Aplicația este statică. Workflow-ul GitHub Actions verifică și publică pe GitHub Pages după actualizarea ramurii main.

https://ccecp.github.io/13-octombrie-2026/

Progresul se păstrează local în browser. Soluțiile există în fișierele statice, iar aplicația este destinată pregătirii, nu administrării securizate a unui examen oficial.

## Seria 51–60: surse și adaptare

200 de întrebări originale. Format 7 verbali + 7 numerici + 6 logici, 60 de minute, patru variante și explicații după finalizare. Variante alfabetice românești, cu punctuație finală și litere mici a, b, c, d. Fără figuri rotite sau oglindite. Include zece matrice simple cu număr de simboluri și reguli explicit precizate.

- Modelele oficiale din 2016: completare verbală; sarcinile figurale rotite au fost cercetate, dar excluse la cererea utilizatoarei. https://www.edu.ro/sites/default/files/Modele%20itemi%20proba%20scrisa_0.pdf
- Modelele din 2017 au fost verificate: documentul consultat conține management și legislație, neincluse în această serie cognitivă. https://edu.ro/sites/default/files/Modele%20itemi%20exemplificativi%20concurs%20dir%20dir%20adj%20iulie%202017_0.pdf
- Subiectul oficial din 15 octombrie 2021: analogii, text și date numerice. https://www.edu.ro/sites/default/files/_fi%C8%99iere/Minister/2021/concursuri/concurs%20directori/subiecte/Concurs_Directori_si_directori_adjuncti_15_octombrie_2021_Varianta_subiect.pdf
- Documentele concursurilor din 18 februarie și 8 septembrie 2022, copii ale subiectelor ministerului: https://cdn.edupedu.ro/wp-content/uploads/2022/02/Concurs_Directori_si_directori_adjuncti_18_februarie_2022_Varianta_subiect.pdf și https://cdn.edupedu.ro/wp-content/uploads/2022/09/Concurs_Directori_si_directori_adjuncti_08_septembrie_2022_Varianta_subiect.pdf
- Descrierea publică a domeniilor de aptitudini la Cognitrom: vocabular, înțelegerea textelor, calcul și raționament. Nu sunt reproduși itemi din bateria profesională. https://www.cognitrom.ro/categorie-produs/teste-psihologice/psihologie-organizationala/aptitudini-cognitive/
- SHL, document public privind capacitatea verbală, numerică, raționamentul deductiv și abstract: https://service.shl.com/docs/Verify%20General%20Ability%20Screen%20Fact%20Sheet.pdf

Exercițiile noi sunt inspirate de tipurile de sarcini descrise public, nu sunt teste clinice standardizate, nu sunt copii ale unei baterii de cabinet și nu prezic subiectele din 2026. Formatul mai vechi cu trei sau cinci alternative a fost adaptat la cele patru alternative cerute pentru 2026; valorile de adevăr din text sunt cerute prin patru combinații de răspuns.

```sh
python scripts/generate_exam_51_60.py
python scripts/validate_exam_51_60.py
```
