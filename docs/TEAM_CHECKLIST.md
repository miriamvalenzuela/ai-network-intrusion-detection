# Team checklist - a page anyone can use to catch up

## What are we building?

We compare four Python machine-learning methods on the **same prepared UNSW-NB15 testing CSV**. Every model predicts `0` for normal traffic or `1` for an attack/suspicious traffic. Person 5 puts the predictions into one simple dashboard. This is a data-analysis project, NOT a tool that monitors real networks.

## If you joined late, do exactly this

1. Download or clone the repo from GitHub.
2. Read the top-level `README.md` and set up `.venv` / install `requirements.txt`.
3. Get the two CSVs into `data/raw/` or generate `data/sample/` for practice.
4. Open **your own folder README** below and run the sample command.
5. Run the real-data command, improve your part, and push your own Git branch.
6. In the group chat, post: **done / next / blocked** and your branch/PR URL.

## What everyone owns

| Person | First file to open | My folder | Result |
|---|---|---|---|
| 1 | `person1_baseline/README.md` | `person1_baseline/` | `results/p1.csv` |
| 2 | `person2_random_forest/README.md` | `person2_random_forest/` | `results/p2.csv` |
| 3 | `person3_svm/README.md` | `person3_svm/` | `results/p3.csv` |
| 4 | `person4_isolation_forest/README.md` | `person4_isolation_forest/` | `results/p4.csv` |
| 5 | `person5_dashboard/README.md` | `person5_dashboard/` | dashboard, screenshot, comparison |

## Week 1: every person independently gets something running

- [ ] Person 1: generate two training-data charts and run the baseline on sample data.
- [ ] Person 2: run Random Forest on sample data, then try real CSV.
- [ ] Person 3: run Linear SVM on sample data, then try real CSV.
- [ ] Person 4: run Isolation Forest on sample data, then try real CSV.
- [ ] Person 5: open working Streamlit page using **fake demo CSVs**.

## Week 2: improve your own code and export output

- [ ] Person 1: prepare summary and `results/p1.csv`.
- [ ] Person 2: test Random Forest and prepare `results/p2.csv`.
- [ ] Person 3: test Linear SVM and prepare `results/p3.csv`.
- [ ] Person 4: test Isolation Forest and prepare `results/p4.csv`.
- [ ] Person 5: show accuracy, precision, recall, F1 and a comparison chart using demo files.

## Week 3: submit, validate, present

- [ ] People 1-4: push their final CSV, README explanation and code in separate PRs.
- [ ] Person 5: load whatever real CSVs are available, validate their row IDs and compare models.
- [ ] Everyone: run `python scripts/validate_results.py` once real results are merged.
- [ ] Everyone: review final demo/report, explain any missing models or limitations truthfully.

## Output agreement (do not change this)

- Training CSV = 175,341 records, testing CSV = 82,332 records.
- For real results, each `results/pN.csv` has `row_id,y_true,y_pred`, 82,332 data rows.
- `row_id` must be 0 to 82,331 in original test order.
- `y_true` and `y_pred` must each contain only 0 or 1.
- Input features must exclude `id`, `label`, `attack_cat`.
- Shared code in `project_utils/` is already provided. No one needs to wait on Person 1 for preprocessing.
- Each person may commit their own folder independently, even if other models are unfinished.

## Message to copy into group chat

```text
Person #:
Done this week:
Working on next:
Blocked by:
Branch or pull request:
```
