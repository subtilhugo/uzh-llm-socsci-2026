# Raw data

No data file in this folder is ever modified; this README is the only file that changes. Cleaned versions are produced by scripts in `code/`
and written to `data/processed/`. The data files themselves are not in the public repository
(`.gitignore`); this README is.

| Folder | Source | What to download | Licence / access | Downloaded on | Status |
| --- | --- | --- | --- | --- | --- |
| `elections/` | Ministère de l'Intérieur, on data.gouv.fr: https://www.data.gouv.fr/datasets/donnees-des-elections-agregees | Results by municipality for the presidential and legislative elections since 2002. Coverage and party labels to verify election by election. | Licence Ouverte | | Session 2 |
| `insee/` | INSEE APIs, catalogue: https://www.insee.fr/fr/information/8184146 (local statistics through the Melodi API) | Population, age structure, unemployment, income, by municipality and year | Licence Ouverte; check whether the chosen API needs a key | | Session 3 (Session 2: files downloaded by hand) |
| `insee/bpe/` | INSEE, Base permanente des équipements | Shops, cafés, services, by municipality and year | Licence Ouverte | | Session 2 |
| `manifestos/` | Manifesto Project: https://manifesto-project.wzb.eu | French party programmes, quasi-sentences with their hand codes | Free academic API key, after registration | | Sessions 3–4 |

## Known pitfalls

- Municipal codes: 5-character strings, leading zeros, Corsica coded 2A/2B.
- Paris, Lyon, Marseille: arrondissements in some files, single municipality in others.
- Municipal mergers (communes nouvelles): the geography changes from year to year.
- Party labels change across elections (FN to RN in 2018, alliance labels in legislative elections).

## Personal data

None: all sources are aggregated at the municipal level or are published programmes.
