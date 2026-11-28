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

- [X] Confirm the CSV files exist and run the sample version.
- [X] Read `train.py` and identify where the Random Forest is created.
- [X] Run `train.py` using real data.

## Week 2 - Train and try one small change

- [X] Open your `results/p2.csv`; verify its columns are `row_id,y_true,y_pred`.
- [ ] Try one small experiment: change `n_estimators` (number of trees) or `max_depth`, then rerun.
- [ ] Write down whether the accuracy, recall or F1 changed.

## Week 3 - Explain and submit

- [ ] Write 3-5 sentences about your approach and result.
- [ ] Include the training-row count and accuracy/precision/recall/F1 values below.
- [ ] Commit your folder and `results/p2.csv` in your own branch.

## Training Rounds and Notes

Training rows used: 30,000
Variables: n_estimators = 100, max_depth = 18
Accuracy: 0.903 | Precision: 0.8641 | Recall: 0.9776 | F1: 0.9174
Conclusion: Baseline run with a subset of data, but even so there is high accuracy and recall.

Training rows used: 175,341
Variables: n_estimators = 100, max_depth = 18
Accuracy: 0.9071 | Precision: 0.8744 | Recall: 0.9708 |F1: 0.9201
Conclusion: More data means a better result, with all else kept equal!

Training rows used: 175,341
Variables: n_estimators = 100, max_depth = 1
Accuracy: 0.7379 | Precision: 0.8289 | Recall: 0.6602 |F1: 0.735
Conclusion: Decreasing the max depth understandably reduced the accuracy and precision drastically.

Training rows used: 175,341
Variables: n_estimators = 100, max_depth = 100
Accuracy: 0.8869 | Precision: 0.8403 | Recall: 0.981 |F1: 0.9052
Conclusion: Dramatically increasing the max_depth parameter doesn't do much past a certain point, and causes a tradeoff between recall and accuracy/precision.

Training rows used: 175,341
Variables: n_estimators = 1000, max_depth = 18
Accuracy: 0.9057 | Precision: 0.8703 | Recall: 0.9709 |F1: 0.919
Conclusion: increasing n_estimators past the default state does not create meaningful change, and comes at the expense of taking longer to run.

Training rows used: 175,341
Variables: n_estimators = 1, max_depth = 18
Accuracy: 0.8933 | Precision: 0.8671 | Recall: 0.9521 |F1: 0.9076
Conclusion: Decreasing n_estimators leads to a less accurate result (as expected).

Training rows used: 175,341
Variables: n_estimators = 100, max_depth = 25
Accuracy: 0.898 | Precision: 0.8576 | Recall: 0.9771 |F1: 0.9134
Conclusion: Increasing max_depth slightly results in better recall/f1, but doesn't positively affect accuracy/precision.

Training rows used: 175,341
Variables: n_estimators = 100, max_depth = 10
Accuracy: 0.9052 | Precision: 0.8724 | Recall: 0.9696 |F1: 0.9184
Conclusion: Less depth provides a better result than the >18 depth

Training rows used: 175,341
Variables: n_estimators = 100, max_depth = 15
Accuracy: 0.9098 | Precision: 0.8787 | Recall: 0.9701 |F1: 0.9222
Conclusion: It did better than I was expecting, and better than the default parameters on most fields

Training rows used: 175,341
Variables: n_estimators = 100, max_depth = 13
Accuracy: 0.9107 | Precision: 0.8815 | Recall: 0.9679 |F1: 0.9227
Conclusion: still improving!

Training rows used: 175,341
Variables: n_estimators = 100, max_depth = 12
Accuracy: 0.9085 | Precision: 0.8778 | Recall: 0.9687 |F1: 0.9210
Conclusion: Decrease detected, so keeping max_depth at 13 and tuning n_estimators next.

Training rows used: 175,341
Variables: n_estimators = 200, max_depth = 13
Accuracy: 0.9096 | Precision: 0.8805 | Recall: 0.9671 |F1: 0.9218
Conclusion: Still not as good results as the 100/13 set, going to try 150 next in hopes that might be better.

Training rows used: 175,341
Variables: n_estimators = 150, max_depth = 13
Accuracy: 0.9104 | Precision: 0.881 | Recall: 0.968 |F1: 0.9225
Conclusion: Still not as good results as the 100/13 set, trying under 100 next.

Training rows used: 175,341
Variables: n_estimators = 50, max_depth = 13
Accuracy: 0.9102 | Precision: 0.881 | Recall: 0.9676 |F1: 0.9223
Conclusion: Results are very similar to 150, suggesting peak range is probably very close to 100.

Training rows used: 175,341
Variables: n_estimators = 125, max_depth = 13
Accuracy: 0.9111 | Precision: 0.8819 | Recall: 0.9683 |F1: 0.923
Conclusion: Best results so far, going to test binary between 100/125

Training rows used: 175,341
Variables: n_estimators = 113, max_depth = 13
Accuracy: 0.9107 | Precision: 0.8815 | Recall: 0.9678 |F1: 0.9227
Conclusion: Less than 125, testing binary between 125/150

Training rows used: 175,341
Variables: n_estimators = 138, max_depth = 13
Accuracy: 0.9106 | Precision: 0.8813 | Recall: 0.9681 |F1: 0.9227
Conclusion: Results are very similar to 113, suggesting peak range is probably very close to 125

Training rows used: 175,341
Variables: n_estimators = 120, max_depth = 13
Accuracy: 0.9108 | Precision: 0.8813 | Recall: 0.9683 |F1: 0.9228
Conclusion: Testing lower side of 125

Training rows used: 175,341
Variables: n_estimators = 130, max_depth = 13
Accuracy: 0.9105 | Precision: 0.8809 | Recall: 0.9684 |F1: 0.9226
Conclusion: Testing higher side of 125. 120 and 125 seems to be a better result than 125 and 130.

Training rows used: 175,341
Variables: n_estimators = 123, max_depth = 13
Accuracy: 0.9109 | Precision: 0.8815 | Recall: 0.9683 |F1: 0.9229
Conclusion: Still higher, only other option is 124.

Training rows used: 175,341
Variables: n_estimators = 124, max_depth = 13
Accuracy: 0.9112 | Precision: 0.8819 | Recall: 0.9683 |F1: 0.9231
Conclusion: Best results so far!

Training rows used: 175,341
Variables: n_estimators = 126, max_depth = 13
Accuracy: 0.9111 | Precision: 0.8818 | Recall: 0.9682 |F1: 0.9230
Conclusion: I expected this one to be worse, and was right. 124/13 is the best combination.

Training rows used: 175,341
Variables: n_estimators = 124, max_depth = 18
Accuracy: 0.9062 | Precision: 0.8733 | Recall: 0.9705 |F1: 0.9193
Conclusion: Confirming that increasing the depth doesn't result in a better result. Recall is improved, but all others are substantially worse.

Training rows used: 175,341
Variables: n_estimators = 124, max_depth = 10
Accuracy: 0.9057 | Precision: 0.8734 | Recall: 0.9692 |F1: 0.9188
Conclusion: Confirming that reducing the depth doesn't result in a better result.

## Final Conclusion
After fine-tuning the model, setting n_estimators to 124 and max_depth to 13 produced the best results, with accuracy of 0.9112, precision of 0.8819, recall of 0.9683, and an F1 score of 0.9231. I initially started training by running experiments with max/min values, to get a general sense for what the metrics may look like under strained circumstances. I then started by using a binary search to place the max_depth value, and once that was set I started adjusting the n_estimators until I found the best possible combination of parameters. To make sure it was truly the best combination, I also ran some sanity tests by adjusting the max_depth again after the n_estimators value was set, to confirm there wasn't any more tuning required.