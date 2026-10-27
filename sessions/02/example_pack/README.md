# Example pack, Session 2

Two raw files. Use them today if you have no structured data of your own.

## How to use it

1. Copy `elections/` and `insee/` into your project's `data/raw/`, so that you have `data/raw/elections/` and `data/raw/insee/`. Keep `extra/` for the bonus.
2. Paste the table below into `data/raw/README.md`.
3. Start Block 1 (prompt 06). A question to start from, if you have none: *is the far-right (RN) first-round vote in 2022 higher in municipalities that lost population?* Change it if you like.

## Provenance

| File | Source | Obtained | Licence / access | Notes |
| --- | --- | --- | --- | --- |
| `elections/resultats-par-niveau-subcom-t1-france-entiere.txt` | Ministère de l'Intérieur, data.gouv.fr, "Election présidentielle des 10 et 24 avril 2022 – Résultats définitifs du 1er tour": https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/ | Downloaded 2026-10-14 | Not stated on the dataset page; the data.gouv.fr default is the Licence Ouverte 2.0. To verify | Final first-round results, one row per municipality. SHA-256 `372243c6…88355` |
| `insee/base-cc-serie-historique-2015.xls` | INSEE, "Chiffres détaillés – Séries historiques" (population censuses 1968–2015 and civil registration), put online 26/06/2018 | Copy from the instructor's archive | INSEE statistics are free to reuse with the source cited. To verify | Several sheets. In this copy, the municipal sheet starts directly with the variable names. SHA-256 `285ba4d8…f7d4085` |
| `extra/v_mvt_commune_2026.csv` | INSEE, Code officiel géographique 2026: history of municipalities (every merger, split, change of name or code since 1943) | Copy from the instructor's archive | INSEE, free reuse with the source cited. To verify | One row per event. For the bonus. SHA-256 `8b339fad…ef8645f1` |

Personal data: none. Both files contain aggregate counts by municipality, and the names of presidential candidates, who are public figures.
