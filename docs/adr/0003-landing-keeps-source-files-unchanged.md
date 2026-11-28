# 0003 Landing keeps source files unchanged

Status: Accepted, 2026-11-28

## Context
The source updates files one or more times a week, mostly adding new match results.
It can also add, delete or reformat files, or change old results, at any time.

## Decision
Landing: files saved as-is, earlier copies kept as storage is cheap.
Each file is marked new, changed, unchanged or missing by comparing its hash; no file is read.
Bronze: changed files are read; new results are expected, anything else is flagged:
format changes, old results or details changed.

## Consequences
Any later step can be rebuilt from the originals, and every change in the source is visible by date.
