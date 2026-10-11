# Pregătim reușita — Concurs directori 2026

Platformă de pregătire în limba română, cu 20 de teste a câte 20 de întrebări (400 de itemi unici).

## Experiența de lucru

- 7 itemi verbali, 7 numerici și 6 logici în fiecare test.
- 60 de minute; termenul se păstrează la reîncărcarea paginii.
- Grilă de navigare, marcarea întrebărilor și verificarea răspunsurilor alese.
- Finalizare confirmată; finalizare automată la expirarea timpului.
- Răspunsurile corecte și explicațiile sunt afișate numai după finalizare.
- 0,5 puncte pentru un răspuns corect; prag de promovare 6/10.
- Explicații pe pași, reguli de reținut, capcane și metode alternative pentru familiile relevante.
- Progres local în browser, posibilitate de reîncepere și tipărirea rezolvărilor.
- Nuanțe de albastru, accente galbene, adaptare la telefon și navigare cu tastatura.

Materiale: Prof. dr. Maria-Magdalena Dorcioman.

## Conținut și surse

Simulările sunt originale și nu reprezintă subiecte oficiale, modele aprobate sau predicții ale subiectelor.

Structura urmează [informarea Ministerului din 29 septembrie 2026](https://edu.ro/press_rel_67_26_informare_probe_concurs_directori).

Interpretarea textelor, analogiile, categoria comună și calculele din tabele adaptează forme prezente în [exemplele oficiale din 2021](https://www.edu.ro/sites/default/files/_fi%C8%99iere/Minister/2021/concursuri/concurs%20directori/Itemi%20exemple%20selectie%20directori.pdf). Formulările și datele sunt noi. Se adaugă subtipuri de pregătire care nu sunt garantate pentru concursul din 2026.

Testele au combinații distincte de subtipuri. Unele familii reapar în contexte diferite: nu pretindem că există 400 de modele psihometrice complet independente. Nu sunt etalonate psihometric.

## Rulare

Aplicația este statică, fără instalare sau construire. Se servește directorul repository-ului prin HTTP; deschiderea directă a `index.html` ca fișier poate bloca încărcarea JSON.

```sh
python -m http.server 8000
```

## GitHub Pages

Workflow-ul `.github/workflows/pages.yml` verifică datele și funcționalitatea, apoi publică fișierele statice. Pentru prima publicare, activați în **Settings → Pages → Build and deployment → Source: GitHub Actions**. La commituri ulterioare pe `main`, publicarea este automată.

Adresa anticipată, după activarea Pages și finalizarea workflow-ului: `https://ccecp.github.io/13-octombrie-2026/`.

## Verificări

```sh
python scripts/validate_content.py
node --check app.js
node scripts/test_app.cjs
```

Validatorul recalculează independent itemii numerici, controlează unicitatea, variantele și structura. Testele aplicației verifică randarea celor 400 de itemi într-un mediu DOM simulat, punctarea, timerul, persistența și separarea dintre examen și rezolvări; nu înlocuiesc o inspecție vizuală în browser.

Generatorul `scripts/generate_tests.py` reproduce banca. După modificarea lui, regenerați datele și rulați verificările.

Datele răspunsurilor sunt păstrate numai în browserul local. Fiind o platformă de antrenament statică, banca de soluții poate fi inspectată în fișierele sursă; aplicația nu este un sistem securizat de examinare oficială.
