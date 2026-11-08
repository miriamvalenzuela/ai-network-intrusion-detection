"""Optional dataset downloader from a public mirror of the official prepared split.

Primary academic dataset page: https://research.unsw.edu.au/projects/unsw-nb15-dataset
Mirror: https://huggingface.co/datasets/Mouwiya/UNSW-NB15-small
If downloading is blocked, visit either page and put the files in data/raw/.
"""
from pathlib import Path
import argparse
import csv
import shutil
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "data" / "raw"
BASE = "https://huggingface.co/datasets/Mouwiya/UNSW-NB15-small/resolve/main/"
EXPECTED = {
    "UNSW_NB15_training-set.csv": 175341,
    "UNSW_NB15_testing-set.csv": 82332,
}


def check_csv(path, expected_rows):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
        if "label" not in header or "attack_cat" not in header:
            raise ValueError(f"Unexpected CSV header in {path.name}: {header[:6]}")
        count = sum(1 for _ in reader)
    if count != expected_rows:
        raise ValueError(f"Expected {expected_rows:,} data rows in {path.name}; found {count:,}")
    print(f"Validated {path.name}: {count:,} rows")


def main():
    parser = argparse.ArgumentParser(description="Download the official UNSW-NB15 prepared split")
    parser.add_argument("--force", action="store_true", help="Redownload even if valid files exist")
    args = parser.parse_args()
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for filename, expected_rows in EXPECTED.items():
        target = DESTINATION / filename
        if target.exists() and not args.force:
            try:
                check_csv(target, expected_rows)
                print("Already downloaded; skipping.")
                continue
            except ValueError:
                print("Existing file is invalid; redownloading it.")
        part = target.with_suffix(".csv.part")
        print(f"Downloading {filename} (this file is about 15-32 MB)...")
        try:
            request = Request(BASE + filename + "?download=true", headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(request, timeout=120) as response, part.open("wb") as output:
                shutil.copyfileobj(response, output)
            check_csv(part, expected_rows)
            part.replace(target)
        except (URLError, HTTPError, OSError, ValueError) as exc:
            part.unlink(missing_ok=True)
            print(f"Download or validation failed for {filename}: {exc}")
            print("Manual fallback: https://research.unsw.edu.au/projects/unsw-nb15-dataset")
            print("or https://huggingface.co/datasets/Mouwiya/UNSW-NB15-small/tree/main")
            print("Place the two CSV files inside data/raw/ and try again.")
            return 1
    print("\nBoth REAL CSV files are available in data/raw/. They are ignored by Git.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
