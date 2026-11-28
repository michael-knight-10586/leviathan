# Runbook: Bronze

## Run (after landing, same day)
1. Workspace → leviathan Git folder → Pull.
2. In a notebook on serverless:
   ```python
   import sys
   user = spark.sql("SELECT current_user()").first()[0]
   sys.path.insert(0, f"/Workspace/Users/{user}/leviathan/src")
   from leviathan.bronze.load import run
   print(run(spark))
   ```
3. Loads only files landed that day (new or changed in the manifest). Prints progress per 50 files.

## Expected
Counts of files, rows, quarantined. In season: a few dozen files.

## If it stops
| Message | Meaning | Action |
|---|---|---|
| ModuleNotFoundError | Old code or stale session | Pull, then `%restart_python`, rerun |
| File not found on a landed_path | Landing incomplete | Rerun landing, then bronze |

Rerunning is always safe: each file's rows are replaced.

## If quarantined > 0
Rows wider than their header. Inspect `leviathan.bronze.matches_quarantine`; silver decides how to use them.
