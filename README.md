# Pregătim reușita — Concurs directori 2026

50 de simulări originale × 20 de itemi (1.000 de itemi), pentru pregătirea probei cognitive din 13 octombrie 2026.

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

Validatorul inițial recalculează primele 400 de întrebări. Controlul suplimentar verifică structura tuturor testelor, unicitatea enunțurilor și identificatorilor, apoi recalculează independent problemele numerice și logice noi din 41–50. Testul aplicației parcurge toate cele 1.000 de întrebări și verifică navigarea, punctarea, persistența, timerul, finalizarea și ascunderea explicațiilor înainte de finalizare.

Reproducerea seriei 41–50:

```sh
python scripts/generate_exam_41_50.py
```

Generatorul necesită Python și Node.js pentru ordonarea variantelor cu collation românească. Nu modifică testele anterioare sau manifestul.

## Publicare

Aplicația este statică. Workflow-ul GitHub Actions verifică și publică pe GitHub Pages după actualizarea ramurii main.

https://ccecp.github.io/13-octombrie-2026/

Progresul se păstrează local în browser. Soluțiile există în fișierele statice, iar aplicația este destinată pregătirii, nu administrării securizate a unui examen oficial.
