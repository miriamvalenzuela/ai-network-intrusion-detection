# Person 3 - Linear Support Vector Machine (SVM)

**Your job in plain English:** Train a model that separates normal and attack traffic using a decision boundary. We use scikit-learn's `LinearSVC` because a full kernel SVM may be too slow on this dataset.

## Start here

```powershell
python scripts/generate_sample_data.py
python person3_svm/train.py --data-dir data/sample
```

With the two official prepared CSV files in `data/raw/`:

```powershell
python person3_svm/train.py
```

The real run saves `results/p3.csv` and `person3_svm/metrics.json`. It starts on a reproducible subset of 30,000 training rows and always predicts the full real test set. Try `--max-train-rows 0` after the starter works if your computer has enough resources.

## Week 1 - Get set up

- [ ] Run the sample version and read `train.py`.
- [ ] Find where the script scales numeric columns and converts categorical columns into numbers.
- [ ] Try a real-data run.

## Week 2 - Train SVM

- [ ] Make `results/p3.csv` with the required three columns.
- [ ] Change the `C` value in `LinearSVC(C=0.5, ...)` and observe the metrics.
- [ ] If you see a convergence warning, mention it and consider a larger `max_iter`.

## Week 3 - Explain and submit

- [ ] Record accuracy, precision, recall, F1 and the training-row count.
- [ ] Write 3-5 sentences on the method, results and training speed.
- [ ] Commit your code, notes and `results/p3.csv`.

## Your notes

Training rows used: TODO

Accuracy: TODO | Precision: TODO | Recall: TODO | F1: TODO

What I learned: TODO

Do not copy anything from the test set into training, including feature-scaling statistics.
