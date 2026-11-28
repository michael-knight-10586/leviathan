"""Manifest: land new or changed source files and record every file's status per run."""

import hashlib
import os
from datetime import date
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from leviathan.landing.discovery import USER_AGENT, compare_pages, discover

TABLE = "leviathan.landing.manifest"
LANDING_ROOT = "/Volumes/leviathan/landing/files/football-data"
MIN_SHARE_OF_LAST_RUN = 0.9  # stop if fewer files than this share of last run are found


def landed_path(url, run_date):
    """Where a file is saved: <site path>/<file stem>/<run date>/<file>.

    .../mmz4281/2627/E0.csv on 2026-11-28 -> LANDING_ROOT/mmz4281/2627/E0/2026-11-28/E0.csv
    """
    site_path = urlparse(url).path.lstrip("/")
    folder, filename = os.path.split(site_path)
    stem = os.path.splitext(filename)[0]
    return f"{LANDING_ROOT}/{folder}/{stem}/{run_date.isoformat()}/{filename}"


def classify(previous, current):
    """Compare last run's hashes with this run's.

    previous, current: dict of url -> sha256.
    Returns dict of url -> status: new, changed, unchanged or missing.
    """
    status = {}
    for url, sha in current.items():
        if url not in previous:
            status[url] = "new"
        elif previous[url] != sha:
            status[url] = "changed"
        else:
            status[url] = "unchanged"
    for url in previous.keys() - current.keys():
        status[url] = "missing"
    return status


def _download(url):
    request = Request(url, headers={"User-Agent": USER_AGENT})
    return urlopen(request, timeout=60).read()


def _create_table(spark):
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            run_date    DATE,
            url         STRING,
            source_page STRING,
            status      STRING,
            sha256      STRING,
            size_bytes  BIGINT,
            landed_path STRING
        )
    """)


def _previous_state(spark, run_date):
    """Last known hash and page of every file still present before this run."""
    rows = spark.sql(f"""
        SELECT url, sha256, source_page FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY url ORDER BY run_date DESC) AS n
            FROM {TABLE} WHERE run_date < DATE'{run_date.isoformat()}'
        ) WHERE n = 1 AND status <> 'missing'
    """).collect()
    return {r.url: r.sha256 for r in rows}, {r.url: r.source_page for r in rows}


def run(spark, run_date=None):
    """Discover, download, compare, land and record. Safe to rerun on the same day."""
    run_date = run_date or date.today()
    _create_table(spark)
    # A rerun replaces the same day's rows, so results are the same however often it runs.
    spark.sql(f"DELETE FROM {TABLE} WHERE run_date = DATE'{run_date.isoformat()}'")

    previous, previous_page_of = _previous_state(spark, run_date)
    pages, files = discover()

    if previous and len(files) < MIN_SHARE_OF_LAST_RUN * len(previous):
        raise RuntimeError(
            f"Found {len(files)} files, last run had {len(previous)}. "
            "Site may have changed; stopping before anything is marked missing."
        )

    content = {url: _download(url) for url, _ in files}
    current = {url: hashlib.sha256(data).hexdigest() for url, data in content.items()}
    status = classify(previous, current)
    page_of = {**previous_page_of, **dict(files)}  # missing files keep their last known page

    rows = []
    for url, state in sorted(status.items()):
        path = None
        if state in ("new", "changed"):
            path = landed_path(url, run_date)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                f.write(content[url])
        data = content.get(url)
        rows.append((run_date, url, page_of.get(url), state, current.get(url),
                     len(data) if data is not None else None, path))

    spark.createDataFrame(rows, schema=spark.table(TABLE).schema).write.mode("append").saveAsTable(TABLE)

    previous_pages = set(previous_page_of.values())
    added_pages, removed_pages = compare_pages(previous_pages, pages) if previous_pages else ([], [])
    summary = {s: sum(1 for v in status.values() if v == s)
               for s in ("new", "changed", "unchanged", "missing")}
    summary["pages_added"], summary["pages_removed"] = added_pages, removed_pages
    return summary
