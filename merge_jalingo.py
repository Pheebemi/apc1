
import csv
import os
from collections import OrderedDict

INPUT_FILES = [
    "jalingo_members.csv",
    "jalingo_members_p76.csv",
    "jalingo_members_p118.csv",
    "jalingo_members_p161.csv",
    "jalingo_members_p199.csv",
]
OUTPUT_FILE = "jalingo_members_FINAL.csv"
FIELDS = ["#", "Member ID", "First Name", "Middle Name", "Last Name", "Phone", "State", "LGA", "Ward"]

print("Merging CSV files...")
seen = set()
all_rows = []

for f in INPUT_FILES:
    if not os.path.exists(f):
        print(f"  MISSING: {f} (skipping)")
        continue
    count = 0
    dupes = 0
    with open(f, "r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            member_id = row.get("Member ID", "").strip()
            if not member_id:
                continue
            if member_id in seen:
                dupes += 1
                continue
            seen.add(member_id)
            all_rows.append(row)
            count += 1
    print(f"  {f}: {count} unique rows added, {dupes} duplicates skipped")

print(f"\nTotal unique records: {len(all_rows):,}")

# Sort by Ward
all_rows.sort(key=lambda r: r.get("Ward", "").strip().upper())

# Re-number the # column
for i, row in enumerate(all_rows, 1):
    row["#"] = i

# Write output
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(all_rows)

print(f"\nSaved to: {os.path.abspath(OUTPUT_FILE)}")

# Summary by ward
ward_counts = {}
for row in all_rows:
    w = row.get("Ward", "UNKNOWN").strip()
    ward_counts[w] = ward_counts.get(w, 0) + 1

print(f"\nRecords by Ward:")
for ward, count in sorted(ward_counts.items()):
    print(f"  {ward}: {count:,}")
