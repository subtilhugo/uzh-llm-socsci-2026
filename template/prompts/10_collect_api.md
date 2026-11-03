# Prompt 10: collect data from an API, and prove the collection is complete

Before pasting: you know which API you want (its documentation URL), and your key is in a file `.env` at the root of the project, one line `NAME_OF_THE_KEY=...`. `.env` is in `.gitignore`: check it with `git check-ignore .env` (it must print `.env`).
Suggested setting: Opus, effort `high`.

---

We collect data from an API into `data/raw/`. You write the collector; I decide what to collect. The collection is not complete because the script ran without error: it is complete when it matches numbers the provider publishes independently of our requests.

1. **Read the documentation first, no code.** Read the API documentation I give you. Tell me, with the page or section for each: the base URL and the endpoints we need; how the key is sent; the parameters; the format of the response; pagination; rate limits; the versions or releases of the data; and the terms of use (redistribution, citation). Then list what you could not find. Wait.
2. **Ask me** what to collect: which units, which period, which fields, which version. Write my answers in `data/raw/README.md` under the source's name, with today's date. If the API offers versions, we pin one.
3. **Find the checks before you write the collector.** Look for numbers the provider publishes on their own: a total count, a list of identifiers, per-unit totals, a published summary dataset. Propose three checks, and how each could fail. Wait for my choice.
4. **Write `code/10_collect_<source>.py`.** It reads the key from `.env` (never prints it, never writes it to a file, never puts it in an error message). It saves every raw response as received, in `data/raw/<source>/<version>/`, before any processing, and never overwrites a file already there. It has a timeout, retries with a pause on HTTP 429 and 5xx, respects the rate limit, follows every page, and logs each request (endpoint, parameters without the key, status, number of items) to `data/raw/<source>/<version>/requests_log.csv`.
5. **Write `code/11_parse_<source>.py`.** It reads only the saved responses and writes one tidy table to `data/processed/`. It prints, and writes to `outputs/collection_checks.md`: requested, returned, listed as missing; the checks I chose in step 3, with the expected and the observed number; empty or duplicated records.
6. **Run both. Show me `outputs/collection_checks.md`.** If a check fails, stop and tell me what you think explains it. Do not fix it on your own.

Rules: no data leaves the folder except the requests we agreed on. If the terms of use forbid something we planned (redistribution, bulk download, a rate), say so before writing code.
