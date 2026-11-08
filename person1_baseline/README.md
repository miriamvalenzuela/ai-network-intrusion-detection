# Person 1 - Dataset exploration and Logistic Regression baseline

**Your job in plain English:** Help everyone understand what is inside the network-traffic dataset, then build a simple classifier. The other models will be compared against yours, but nobody needs to wait for you to finish.

## Start here

From the repo root, after installing `requirements.txt`:

```powershell
python scripts/generate_sample_data.py
python person1_baseline/analyze.py --data-dir data/sample
python person1_baseline/train.py --data-dir data/sample
```

These use **fake practice data**, creating sample charts and predictions in ignored `scratch/` files. For the actual assignment, get the real dataset into `data/raw/` first:

```powershell
python person1_baseline/analyze.py
python person1_baseline/train.py
```

Your predictions go to `results/p1.csv`, your metric values to `person1_baseline/metrics.json`, and real-data charts to `person1_baseline/figures/`.

## Week 1 - Understand the dataset

- [ ] Run `analyze.py` on the real CSVs.
- [ ] Look at `figures/class_counts.png` and `figures/missing_values.png`.
- [ ] Replace the TODO line in `dataset_summary.md` with 3-5 sentences about what the records contain and what you noticed.

## Week 2 - Build baseline

- [ ] Run `train.py` using the real data.
- [ ] Open `results/p1.csv` and confirm its column names.
- [ ] For extra effort, compare 30,000 training rows with `--max-train-rows 0` (all rows).

## Week 3 - Explain and submit

- [ ] Record accuracy, precision, recall, F1 and training-row count in this README.
- [ ] Explain what worked, what surprised you and one limitation.
- [ ] Commit your script, charts, written summary and `results/p1.csv` on your own branch.

## Your notes (fill these in)

Training rows used: TODO

Accuracy: TODO | Precision: TODO | Recall: TODO | F1: TODO

What I learned: TODO

**Do not commit** the CSV datasets in `data/raw/`, and do not report synthetic sample metrics as real results.
