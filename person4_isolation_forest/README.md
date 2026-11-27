# Person 4 - Isolation Forest anomaly detection

**Your job in plain English:** Instead of learning attack labels, your algorithm learns what **normal** traffic looks like, then marks unusual-looking records as suspicious. An unusual record is not automatically a confirmed cyberattack.

## Start here

```powershell
python scripts/generate_sample_data.py
python person4_isolation_forest/train.py --data-dir data/sample
```

When the real prepared CSVs have been downloaded into `data/raw/`:

```powershell
python person4_isolation_forest/train.py
```

The model trains only on rows with `label=0` from the training CSV. It ignores attack labels during fit. The script uses only numeric features for simplicity. `IsolationForest.predict()` uses `+1` for typical records, `-1` for anomalies; the script converts that to the common team contract `0=normal`, `1=suspicious`.

## Week 1 - Get set up

- [X] Run the synthetic sample once.
- [X] Find `X_normal = X_train.loc[y_train == 0]` in `train.py`.
- [X] Confirm the official dataset is downloaded and run with real data.

## Week 2 - Train anomaly detector

- [X] Save `results/p4.csv` with the required three columns.
- [X ] Try a different `contamination` value (for example `0.01`), then compare results.

contamination = 0.02
  "accuracy": 0.4936,
  "precision": 0.8816,
  "recall": 0.0926,
  "f1": 0.1677,
  "training_data": "UNSW_NB15",
  "test_rows": 82332

contamination = 0.01
  "accuracy": 0.4588,
  "precision": 0.7939,
  "recall": 0.0229,
  "f1": 0.0446,
  "training_data": "UNSW_NB15",
  "test_rows": 8233

When 'contamination' was set to 0.01, it detected fewer attacks, with all of the evaluation metrics (accruacy, precision, recall, f1) lower than when 'contamination' was set to 0.02. 

- [X] Explain in simple terms why anomalies might include normal activity and miss some attacks.

Anomalies might incldue normal activity and miss some attacks due to false positives and false negatives. Normal activity doesn't necessarily mean that the activity happens often/is seen often, so therefore that could be a false positive, meaning that the activity is flagged as an attack. An isolation forest is meant to flag anything that seems unusual, so if normal activity doesn't happen often enough, it can be considered unusual. In a similar fashion, an attack that looks common, the isolation forest might not flag it, leading to a false negative.

## Week 3 - Explain and submit

- [ ] Record accuracy, precision, recall, F1 and the normal training-row count.
- [ ] Write 3-5 sentences about how your unsupervised approach compares to classification.
- [ ] Commit your files and `results/p4.csv`.

## Your notes

Normal training rows used: TODO

Accuracy: TODO | Precision: TODO | Recall: TODO | F1: TODO

What I learned: TODO

`contamination` is a modeling assumption. Do not pick it based on test-set labels if claiming an unbiased final test evaluation.
