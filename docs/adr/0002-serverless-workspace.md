# 0002 Serverless workspace

Status: Accepted, 2026-11-24

## Context
leviathan needs Databricks compute for a small weekly ingestion.

## Options considered
Serverless: no clusters or networking to manage; pay per run.
Classic: own clusters; needed only for GPUs, ML runtime, Scala/R.

## Decision
Serverless, the easiest default option.

## Consequences
Code reaches storage only through Unity Catalog names, never Azure storage addresses.
