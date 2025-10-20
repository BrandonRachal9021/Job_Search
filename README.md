This project includes a CSV cleaner/filter for job listings.

### Features
- Remove duplicate listings (Job Title + Company + Location).
- Parse and sort by `Date Posted`.
- Filter by date, location, and title/company keywords.
- Drop listings older than **N** days.
- Export to cleaned CSV and optional JSON.

### Usage
```bash
python3 jobs_tool.py --dedup --sort-desc
python3 jobs_tool.py --min-date "Oct 10 2025" --sort-desc -o jobs_recent.csv
python3 jobs_tool.py --drop-older-than 7 --sort-desc -o jobs_last7.csv
python3 jobs_tool.py --location "New Orleans" -o jobs_nola.csv
python3 jobs_tool.py --title-contains "engineer" --company-contains "Acme" -o jobs_acme_eng.csv
python3 jobs_tool.py --dedup --sort-desc --json jobs.json
