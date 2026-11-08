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

- [ ] Run the synthetic sample once.
- [ ] Find `X_normal = X_train.loc[y_train == 0]` in `train.py`.
- [ ] Confirm the official dataset is downloaded and run with real data.

## Week 2 - Train anomaly detector

- [ ] Save `results/p4.csv` with the required three columns.
- [ ] Try a different `contamination` value (for example `0.01`), then compare results.
- [ ] Explain in simple terms why anomalies might include normal activity and miss some attacks.

## Week 3 - Explain and submit

- [ ] Record accuracy, precision, recall, F1 and the normal training-row count.
- [ ] Write 3-5 sentences about how your unsupervised approach compares to classification.
- [ ] Commit your files and `results/p4.csv`.

## Your notes

Normal training rows used: TODO

Accuracy: TODO | Precision: TODO | Recall: TODO | F1: TODO

What I learned: TODO

`contamination` is a modeling assumption. Do not pick it based on test-set labels if claiming an unbiased final test evaluation.
