# 0004 Bronze keeps rows as text maps

Status: Accepted, 2026-11-28

## Context
Source files differ in columns, encodings and quality; bronze must hold them faithfully.

## Options considered
Wide: one column per source column (~190), as the archive did.
Map: each row stored as column name → value text.

## Decision
One table, leviathan.bronze.matches; each row a map of the file's own column names to text values,
with url, landed_path, run_date, encoding and row number. A changed file's rows are replaced.
Rows wider than the header go to leviathan.bronze.matches_quarantine. Repeated names kept as X#2.

## Consequences
New or odd source columns need no change; column naming is done once, in silver.
