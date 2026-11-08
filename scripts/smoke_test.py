"""Quick end-to-end test: create FAKE data, run all four starters, check outputs."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    ["scripts/generate_sample_data.py"],
    ["person1_baseline/analyze.py", "--data-dir", "data/sample"],
    ["person1_baseline/train.py", "--data-dir", "data/sample"],
    ["person2_random_forest/train.py", "--data-dir", "data/sample"],
    ["person3_svm/train.py", "--data-dir", "data/sample"],
    ["person4_isolation_forest/train.py", "--data-dir", "data/sample"],
    ["scripts/validate_results.py", "--results-dir", "scratch/sample_results"],
]


def main():
    for args in COMMANDS:
        command = [sys.executable] + args
        print("\nRUN:", " ".join(command), flush=True)
        subprocess.run(command, cwd=ROOT, check=True)
    print("\nSUCCESS: all four starter models ran on synthetic sample data.")
    print("Synthetic data and predictions are ignored by Git; not final results.")


if __name__ == "__main__":
    main()
