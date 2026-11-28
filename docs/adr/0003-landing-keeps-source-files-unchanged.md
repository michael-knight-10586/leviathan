# 0003 Landing keeps source files unchanged

Status: Accepted, 2026-11-28

## Context
The source updates files one or more times a week, mostly adding new match results.
It can also add, delete or reformat files, or change old results, at any time.

## Decision
Files saved as-is, with earlier copies kept as storage is cheap. New results are expected;
anything else (format changes, files added or missing, results or details changed) is flagged.

## Consequences
Any later step can be rebuilt from the originals, and every change in the source is visible by date.
