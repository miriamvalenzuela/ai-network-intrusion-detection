"""Check basic Python environment and where the prepared dataset should go."""
from pathlib import Path
import importlib
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ["numpy", "pandas", "sklearn", "matplotlib", "streamlit"]


def main():
    print("Python:", sys.version.split()[0])
    if sys.version_info < (3, 10):
        print("WARNING: use Python 3.11 or 3.12 for the easiest setup.")
    missing = []
    for package in PACKAGES:
        try:
            module = importlib.import_module(package)
            print(f"  OK: {package} {getattr(module, '__version__', '')}")
        except ImportError:
            missing.append(package)
            print(f"  MISSING: {package}")
    if missing:
        print("\nInstall packages: python -m pip install -r requirements.txt")
    for directory in ("data/raw", "data/sample"):
        path = ROOT / directory
        print(f"\n{directory}:")
        for name in ("UNSW_NB15_training-set.csv", "UNSW_NB15_testing-set.csv"):
            p = path / name
            print(f"  {'OK' if p.exists() else 'NOT FOUND'}: {name}")
    print("\nNo CSV files? Run: python scripts/generate_sample_data.py")
    print("For real data: python scripts/download_dataset.py")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
