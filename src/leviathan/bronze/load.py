"""Bronze load: read files landed this run into leviathan.bronze.matches, unchanged."""

import csv
import io
from datetime import date

from leviathan.landing.manifest import TABLE as MANIFEST

MATCHES = "leviathan.bronze.matches"
QUARANTINE = "leviathan.bronze.matches_quarantine"
ENCODINGS = ("utf-8-sig", "cp1252")  # tried in order; latin-1 is the last resort
FILES_PER_BATCH = 50


def decode(raw):
    """Turn file bytes into text. Returns (text, encoding used)."""
    for encoding in ENCODINGS:
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            pass
    return raw.decode("latin-1"), "latin-1"  # never fails: every byte maps to a character


def parse(text):
    """Split CSV text into good rows and bad rows.

    Returns (records, bad):
      records: list of (row_no, {column name: value}) for rows that fit the header
      bad:     list of (row_no, raw line, reason) for rows that don't
    Values are kept exactly as text. Blank rows are skipped.
    """
    lines = text.splitlines()
    rows = [next(csv.reader([line]), []) for line in lines]  # one row per line, kept aligned
    if not rows:
        return [], []

    header = [name.strip() for name in rows[0]]
    while header and header[-1] == "":
        header.pop()  # trailing commas make empty column names
    header = _unique(header)

    records, bad = [], []
    for row_no, (line, row) in enumerate(zip(lines[1:], rows[1:]), start=1):
        if not any(field.strip() for field in row):
            continue
        while len(row) > len(header) and row[-1].strip() == "":
            row = row[:-1]  # trailing empty fields beyond the header are harmless
        if len(row) > len(header):
            bad.append((row_no, line, "more fields than header"))
            continue
        records.append((row_no, dict(zip(header, row))))
    return records, bad


def _unique(names):
    """Keep every column even if a name repeats: second 'X' becomes 'X#2'."""
    seen, out = {}, []
    for name in names:
        seen[name] = seen.get(name, 0) + 1
        out.append(name if seen[name] == 1 else f"{name}#{seen[name]}")
    return out


def _create_tables(spark):
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {MATCHES} (
            url         STRING,
            landed_path STRING,
            run_date    DATE,
            encoding    STRING,
            row_no      INT,
            record      MAP<STRING, STRING>
        )
    """)
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {QUARANTINE} (
            url         STRING,
            landed_path STRING,
            run_date    DATE,
            row_no      INT,
            raw_line    STRING,
            reason      STRING
        )
    """)


def run(spark, run_date=None):
    """Load every file landed on run_date. A changed file's old rows are replaced.

    Safe to rerun: each file's rows are deleted before its new rows are added.
    """
    run_date = run_date or date.today()
    _create_tables(spark)
    landed = spark.sql(f"""
        SELECT url, landed_path FROM {MANIFEST}
        WHERE run_date = DATE'{run_date.isoformat()}' AND status IN ('new', 'changed')
        ORDER BY url
    """).collect()

    totals = {"files": len(landed), "rows": 0, "quarantined": 0}
    for start in range(0, len(landed), FILES_PER_BATCH):
        batch = landed[start:start + FILES_PER_BATCH]
        good_rows, bad_rows = [], []
        for f in batch:
            with open(f.landed_path, "rb") as fh:
                text, encoding = decode(fh.read())
            records, bad = parse(text)
            good_rows += [(f.url, f.landed_path, run_date, encoding, n, r) for n, r in records]
            bad_rows += [(f.url, f.landed_path, run_date, n, line, why) for n, line, why in bad]

        urls = ", ".join(f"'{f.url}'" for f in batch)
        spark.sql(f"DELETE FROM {MATCHES} WHERE url IN ({urls})")
        spark.sql(f"DELETE FROM {QUARANTINE} WHERE url IN ({urls})")
        if good_rows:
            spark.createDataFrame(good_rows, spark.table(MATCHES).schema) \
                .write.mode("append").saveAsTable(MATCHES)
        if bad_rows:
            spark.createDataFrame(bad_rows, spark.table(QUARANTINE).schema) \
                .write.mode("append").saveAsTable(QUARANTINE)

        totals["rows"] += len(good_rows)
        totals["quarantined"] += len(bad_rows)
        print(f"{start + len(batch)}/{len(landed)} files loaded")
    return totals
