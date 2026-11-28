# Runbook: Landing

## Run (until the weekly job exists)
1. Workspace → leviathan Git folder → Pull.
2. In a notebook on serverless:
   ```python
   import sys
   user = spark.sql("SELECT current_user()").first()[0]
   sys.path.insert(0, f"/Workspace/Users/{user}/leviathan/src")
   from leviathan.landing.manifest import run
   print(run(spark))
   ```
3. Takes about 15–30 minutes (to be confirmed).

## Expected
Summary of counts: new / changed / unchanged / missing, plus pages_added / pages_removed.
First run: all new. In season: a few dozen changed, the rest unchanged.

## If it stops
| Message | Meaning | Action |
|---|---|---|
| "Found N files, last run had M" | Site may have been redesigned | Open data.php; check country links still say "Football Results" |
| Page or download error | Site down or throttling | Rerun later |
| Runs much longer than usual | Site throttling | Stop it, rerun later |

Rerunning is always safe: the same day's rows are replaced.

## If the summary shows
| Value | Meaning | Action |
|---|---|---|
| pages_added / pages_removed | Site added or dropped a country | Check by hand |
| missing > 0 | Files removed from the site | Last copy kept in landing |
