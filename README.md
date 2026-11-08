# AI Network Intrusion Detection System

**Starter repository for a five-person, three-week class project.** We use the prepared UNSW-NB15 dataset to compare four methods for classifying a network-traffic record as **normal (0)** or **an attack (1)**. This is an offline student ML experiment, not a live intrusion-prevention tool.

> New to the project? Start here, then read only your person's README. You do not need to understand every teammate's model to begin.

## Who works on what?

| Person | Folder | Job | Final result |
|---|---|---|---|
| 1 | `person1_baseline/` | Explore the dataset and train Logistic Regression | `results/p1.csv` + charts + summary |
| 2 | `person2_random_forest/` | Train Random Forest | `results/p2.csv` + explanation |
| 3 | `person3_svm/` | Train a linear SVM | `results/p3.csv` + explanation |
| 4 | `person4_isolation_forest/` | Train an anomaly detector using normal-only rows | `results/p4.csv` + explanation |
| 5 | `person5_dashboard/` | Compare predictions in a Streamlit dashboard | app, screenshot, conclusion |

Each person edits **only their folder and their own results CSV**. The `project_utils/` folder is a ready-made, stable helper and is **not** someone's weekly assignment. Everyone can start without waiting for another person's code.

## FIRST-TIME SETUP (Windows PowerShell, from the repo root)

1. Install **Git**, **Python 3.11** (or 3.12), and **VS Code**. In PowerShell check `git --version` and `py -3.11 --version` (or `py -3.12 --version`).
2. Clone the repo from the green **Code > HTTPS** button on GitHub. Example (replace URL):

   ```powershell
   cd $HOME\Documents
   git clone https://github.com/OWNER/REPO.git
   cd REPO
   ```

3. The repo owner should unzip the starter files **into this folder** (alongside the existing three-week plan PDFs/MD files), then commit and merge the starter once. All other members should just `git pull origin main` after that.
4. Create a local Python environment (each teammate does this on their own computer):

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   python scripts/check_setup.py
   ```

   If activation is blocked, use `Set-ExecutionPolicy -Scope Process Bypass` and try activation again. This applies only to the current PowerShell session. Or use `.\.venv\Scripts\python.exe` in place of `python` and skip activation.

5. **First success without a big download:**

   ```powershell
   python scripts/generate_sample_data.py
   python person2_random_forest/train.py --data-dir data/sample
   python scripts/validate_results.py --results-dir scratch/sample_results
   streamlit run person5_dashboard/app.py
   ```

   The sample CSVs are **synthetic practice data**; their scores are **not** evidence for the final report. The demo outputs go into ignored `scratch/` files, not `results/`.

6. **Get the real dataset:**

   ```powershell
   python scripts/download_dataset.py
   ```

   If the mirror blocks automated downloads, download the two **prepared** CSVs manually from the [UNSW dataset page](https://research.unsw.edu.au/projects/unsw-nb15-dataset) or this [public mirror](https://huggingface.co/datasets/Mouwiya/UNSW-NB15-small/tree/main). Put both CSVs in `data/raw/` with their original filenames. They should be:

   - `data/raw/UNSW_NB15_training-set.csv` (175,341 data rows)
   - `data/raw/UNSW_NB15_testing-set.csv` (82,332 data rows)

   The original dataset is not included in this ZIP and is ignored by Git, avoiding large and potentially restricted uploads. Academic users should cite the original authors; details are in `data/README.md`.

7. **Run your assigned real-data script** from the repository root:

   ```powershell
   python person1_baseline/analyze.py
   python person1_baseline/train.py
   python person2_random_forest/train.py
   python person3_svm/train.py
   python person4_isolation_forest/train.py
   python scripts/validate_results.py
   streamlit run person5_dashboard/app.py
   ```

   Run **only the line(s) for your assigned role**. Each default model uses up to 30,000 training rows to make the initial run easier; it still predicts **every row in the official 82,332-row test CSV**. When comfortable, add `--max-train-rows 0` to train on the entire training set (may take longer). Record your actual training subset size in your report.

## Repository layout

```text
REPO/
|-- README.md                  <- start here
|-- QUICKSTART_WINDOWS.md     <- Windows first-time guide
|-- CONTRIBUTING.md           <- Git branches, commits, pull requests
|-- requirements.txt          <- libraries everyone installs
|-- data/
|   |-- raw/                  <- real UNSW CSVs (do NOT commit)
|   |-- sample/               <- small generated test CSVs (do NOT commit)
|   `-- README.md
|-- project_utils/core.py     <- stable CSV/preprocessing/output helpers
|-- scripts/                  <- setup, sample data, downloader, validator
|-- person1_baseline/         <- Person 1 files
|-- person2_random_forest/    <- Person 2 files
|-- person3_svm/              <- Person 3 files
|-- person4_isolation_forest/ <- Person 4 files
|-- person5_dashboard/        <- Person 5 files + fake demo results
|-- results/                  <- real predictions p1.csv ... p4.csv (COMMIT)
`-- scratch/                  <- ignored sample runs
```

Your repo's existing `Network_Intrusion_Project_3_Week_Async_Plan.pdf` and `.md` can stay in the top level. This kit does not replace them.

## How predictions connect everyone

Every model writes exactly three columns, in the ORIGINAL test-row order:

```csv
row_id,y_true,y_pred
0,0,0
1,1,1
2,1,0
```

`row_id` counts from 0; `y_true` is the real test-set label; `y_pred` is the model's prediction. Results for the full real dataset must have 82,332 data rows. `project_utils/core.py` writes this automatically; do not rename columns or shuffle test rows. Person 5 simply reads whichever CSVs exist in `results/`.

## What goes into GitHub?

**Commit:** Python scripts, Markdown instructions, small charts/metrics, and the four final `results/p1.csv` through `p4.csv` files. **Never commit:** `.venv/`, the large `data/raw/` files, generated `data/sample/` files, `scratch/`, passwords, or model binaries. These are already listed in `.gitignore`.

## Need to catch up?

1. Read this README and `docs/TEAM_CHECKLIST.md`.
2. Find your folder and read its README.
3. Make sure `python scripts/check_setup.py` reports installed libraries.
4. Run the sample command for your person, then run the real command.
5. Edit your own script/README, commit your work, and post **done / next / blocked**.

See `CONTRIBUTING.md` for exact commands and `docs/TROUBLESHOOTING.md` if a command fails.
