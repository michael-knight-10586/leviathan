# leviathan

Leviathan ingests all football match data from football-data.co.uk, for every country, division and season. It lands source files unchanged, loads them into bronze, and conforms them in silver, using canonical division codes and a consistent column naming grammar. It refreshes weekly and incrementally. Every row traces to its source file, and reruns are idempotent. Leviathan does no analysis. Analysis happens downstream, in serena and aisha, which read leviathan's silver tables.

## Landing

Weekly copy of every file on football-data.co.uk, saved unchanged (ADR 0003).

Files: `/Volumes/leviathan/landing/files/football-data/<site path>/<file stem>/<date>/<file>`

- `mmz4281/2627/E0/2026-11-28/E0.csv` main leagues, one file per division per season
- `new/ARG/2026-11-28/ARG.csv` extra leagues, one file per country, all seasons
- `mmz4281` and `new` are the site's own folder names.
- A new dated copy only when a file changed.

Table: `leviathan.landing.manifest`, one row per file per run

- status: new · changed · unchanged · missing (missing recorded once)
- columns: run_date, url, source_page, status, sha256, size_bytes, landed_path

Code: `src/leviathan/landing/` (`discovery.py` finds files, `manifest.py` lands and records)
