# Real model prediction files

Only the official UNSW-NB15 test-set predictions go here:

- `p1.csv` = Person 1 Logistic Regression
- `p2.csv` = Person 2 Random Forest
- `p3.csv` = Person 3 Linear SVM
- `p4.csv` = Person 4 Isolation Forest

All four files must have exactly:

```csv
row_id,y_true,y_pred
0,0,0
1,1,1
```

For the actual project: 82,332 data rows, original testing CSV order, binary labels 0 or 1. Check with `python scripts/validate_results.py` from the repo root. These small prediction outputs are intentionally **not ignored by Git**. Do NOT place the training/testing datasets in here.

Synthetic sample predictions belong only in ignored `scratch/sample_results/`.
