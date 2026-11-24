# 0001 Engineered football data

Status: Accepted, 2026-11-24

## Context
Pre-match football analysis uses this data prepared in a standard format.

## Decision
leviathan ingests data. Analysis in separate projects consumes it without needing to format again.

## Consequences
Analysis projects depend on leviathan's silver columns, allowing them to be easily compared.
