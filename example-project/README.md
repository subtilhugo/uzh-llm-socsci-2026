# Who votes far right? The local rise of the FN/RN in France

Example project of the workshop. It is the state of the project after Session 1: the context is filled,
the literature is listed. The literature notes, the memo and the critique are added after the live demo.

## Research question

Why has the vote for the Front National / Rassemblement National grown faster in some French
municipalities than in others? We look at two things: the local conditions in which the vote rose
(economic decline, trade exposure, the closing of local services and places of sociability,
demographic change), and what parties say about these conditions in their programmes.

## Design

- **Unit of analysis:** the municipality (commune), identified by its INSEE code.
- **Period:** presidential and legislative elections, from 2002 to 2024. To decide once we know which
  elections are available at the municipal level with consistent party labels.
- **Outcome:** FN/RN vote share in the first round, as a share of valid votes (exprimés).
- **Explanatory variables:** local indicators from INSEE: population change, age structure, unemployment,
  income, share of industrial jobs, presence of shops and services (Base permanente des équipements).
- **Comparison:** changes within municipalities over time (municipality and election fixed effects).
  Descriptive at this stage: no causal claim until an identification strategy is chosen.
- **Text:** party programmes, to measure what the FN/RN and other parties say about local decline,
  public services, trade and immigration.

## Data

| Source | What it contains | Where it lives | Access / licence | Session |
| --- | --- | --- | --- | --- |
| Ministère de l'Intérieur, election results | Results by municipality (and polling station), by candidate or list | `data/raw/elections/` | data.gouv.fr, Licence Ouverte | 2 |
| INSEE local statistics | Population, age, employment, income, by municipality | `data/raw/insee/` | INSEE APIs (catalogue on insee.fr), Licence Ouverte | 2–3 |
| INSEE Base permanente des équipements | Shops, cafés, services, by municipality and year | `data/raw/insee/bpe/` | insee.fr, Licence Ouverte | 2 |
| Manifesto Project | French party programmes, split into quasi-sentences and hand-coded | `data/raw/manifestos/` | API, free academic key | 3–4 |

Details, URLs and access conditions in `data/raw/README.md`.

## Literature

Six works this project builds on. Full references in `literature/README.md`; one note per work in
`notes/literature/` (written by the agent from the PDF, then verified).

- **Subtil (2026), *Betting Alone: Café Closures and Far-Right Voting in France*.** Café closures and the
  far-right vote: the loss of places of encounter as a channel. Our own paper; the design to compare with.
- **Colantone & Stanig (2018, AJPS).** Import competition from China and nationalist, radical-right voting
  in Western European regions. The trade-exposure channel.
- **Autor, Dorn, Hanson & Majlesi (2020, AER).** Trade exposure and political polarisation in the United States.
  The same channel, with a shift-share design to learn from.
- **Guriev & Papaioannou (2022, JEL).** A survey of the political economy of populism: economic and cultural
  drivers, and the evidence for each. The map in which the project sits.
- **Coquard (2019), *Ceux qui restent*.** Ethnography of young adults in declining rural areas of eastern France.
  What "those who stay" live through, and why the RN speaks to them.
- **Ternullo (2024), *How the Heartland Went Red*.** Why local institutions (unions, churches, civic life)
  shape how places shift to the right in an age of nationalised politics.

## How this project runs through the workshop

| Session | What the project gains |
| --- | --- |
| 1 (14 Oct) | This folder, literature notes, a research memo, a hostile critique |
| 2 (28 Oct) | Election results and INSEE indicators, cleaned and merged by municipality; first figures |
| 3 (4 Nov) | INSEE data through the API; programmes through the Manifesto Project API; dictionary and embedding measures |
| 4 (18 Nov) | Annotation of programme sentences with a paid and a local LLM, validated against the Manifesto codes |
| 5 (2 Dec) | Scanned candidates' leaflets (professions de foi) and debate audio, turned into a corpus |

## People

Hugo Subtil (University of Zurich), instructor of the workshop.
