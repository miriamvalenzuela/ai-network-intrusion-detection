# Person 2 - Random Forest classifier

**Your job in plain English:** A Random Forest combines many decision trees. Your part is to train one, see how well it recognizes attack vs. normal network traffic, and compare its result to other models later.

## Start here

From the repo root, with Python requirements installed:

```powershell
python scripts/generate_sample_data.py
python person2_random_forest/train.py --data-dir data/sample
```

When the two real CSVs are in `data/raw/`:

```powershell
python person2_random_forest/train.py
```

The real run produces `results/p2.csv` and `person2_random_forest/metrics.json`. Sample runs go to ignored `scratch/`. Start with 30,000 training records to avoid long first runs; pass `--max-train-rows 0` to use all training records later.

## Week 1 - Get a working starting script

- [ ] Confirm the CSV files exist and run the sample version.
- [ ] Read `train.py` and identify where the Random Forest is created.
- [ ] Run `train.py` using real data.

## Week 2 - Train and try one small change

- [ ] Open your `results/p2.csv`; verify its columns are `row_id,y_true,y_pred`.
- [ ] Try one small experiment: change `n_estimators` (number of trees) or `max_depth`, then rerun.
- [ ] Write down whether the accuracy, recall or F1 changed.

## Week 3 - Explain and submit

- [ ] Write 3-5 sentences about your approach and result.
- [ ] Include the training-row count and accuracy/precision/recall/F1 values below.
- [ ] Commit your folder and `results/p2.csv` in your own branch.

## Your notes

Training rows used: TODO

Accuracy: TODO | Precision: TODO | Recall: TODO | F1: TODO

What I changed and learned: TODO

Do not edit another teammate's folder or use `label`/`attack_cat` as input features.
