import csv, argparse, sys, json
from datetime import datetime, timedelta
from pathlib import Path

DATE_FORMATS = [
    "%b %d %Y",    # Oct 19 2025
    "%b %d, %Y",   # Oct 19, 2025
    "%Y-%m-%d",    # 2025-10-19
]

HEADERS = ["Job Title", "Company", "Location", "Date Posted"]

def parse_date(s):
    if not s: return None
    s = s.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None

def read_jobs(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        # Ensure headers exist; attempt to remap if needed
        missing = [h for h in HEADERS if h not in r.fieldnames]
        if missing:
            print(f"⚠️ CSV missing expected headers: {missing}", file=sys.stderr)
        for row in r:
            item = {h: row.get(h, "").strip() for h in HEADERS}
            item["_date"] = parse_date(item["Date Posted"])
            rows.append(item)
    return rows

def write_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        for r in rows:
            w.writerow({h: r.get(h, "") for h in HEADERS})

def write_json(rows, path):
    data = [{h: r.get(h, "") for h in HEADERS} for r in rows]
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")

def dedup(rows):
    seen, out = set(), []
    for r in rows:
        key = (r["Job Title"].lower(), r["Company"].lower(), r["Location"].lower())
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out

def filter_rows(rows, args):
    out = rows
    if args.location:
        loc_key = args.location.lower()
        out = [r for r in out if loc_key in r["Location"].lower()]
    if args.title_contains:
        tkey = args.title_contains.lower()
        out = [r for r in out if tkey in r["Job Title"].lower()]
    if args.company_contains:
        ckey = args.company_contains.lower()
        out = [r for r in out if ckey in r["Company"].lower()]
    if args.min_date:
        md = parse_date(args.min_date)
        if md:
            out = [r for r in out if r["_date"] and r["_date"] >= md]
    if args.drop_older_than is not None:
        cutoff = datetime.now().date() - timedelta(days=args.drop_older_than)
        out = [r for r in out if r["_date"] and r["_date"] >= cutoff]
    return out

def sort_rows(rows, desc=True):
    return sorted(rows, key=lambda r: (r["_date"] or datetime(1900,1,1).date()), reverse=desc)

def main():
    p = argparse.ArgumentParser(description="Clean/filter/sort job listings CSV.")
    p.add_argument("--input", "-i", default="fake_jobs.csv", help="Input CSV filename")
    p.add_argument("--output", "-o", default="fake_jobs_clean.csv", help="Output CSV filename")
    p.add_argument("--json", help="Optional JSON output filename")
    p.add_argument("--dedup", action="store_true", help="Remove duplicate listings")
    p.add_argument("--sort-desc", action="store_true", help="Sort by Date Posted (newest first)")
    p.add_argument("--sort-asc", action="store_true", help="Sort by Date Posted (oldest first)")
    p.add_argument("--min-date", help='Keep rows on/after this date (e.g., "Oct 10 2025")')
    p.add_argument("--drop-older-than", type=int, help="Drop rows older than N days from today")
    p.add_argument("--location", help="Keep rows whose Location contains this substring")
    p.add_argument("--title-contains", help="Keep rows whose Job Title contains this substring")
    p.add_argument("--company-contains", help="Keep rows whose Company contains this substring")
    args = p.parse_args()

    rows = read_jobs(args.input)
    if args.dedup:
        rows = dedup(rows)
    rows = filter_rows(rows, args)

    if args.sort_desc:
        rows = sort_rows(rows, desc=True)
    elif args.sort_asc:
        rows = sort_rows(rows, desc=False)

    write_csv(rows, args.output)
    if args.json:
        write_json(rows, args.json)

    print(f"✅ Wrote {len(rows)} rows to {args.output}" + (f" and {args.json}" if args.json else ""))

if __name__ == "__main__":
    main()