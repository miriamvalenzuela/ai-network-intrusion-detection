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
- [X] Try a different `contamination` value (for example `0.01`), then compare results.

contamination = 0.02
  "accuracy": 0.4936,
  "precision": 0.8816,
  "recall": 0.0926,
  "f1": 0.1677,
  "training_data": "UNSW_NB15"

contamination = 0.01
  "accuracy": 0.4588,
  "precision": 0.7939,
  "recall": 0.0229,
  "f1": 0.0446,
  "training_data": "UNSW_NB15"

contamination = 0.05 
  "accuracy": 0.5592,
  "precision": 0.8468,
  "recall": 0.2435,
  "f1": 0.3783,
  "training_data": "UNSW_NB15"


When 'contamination' was set to 0.01, it detected fewer attacks, with all of the evaluation metrics (accruacy, precision, recall, f1) lower than when 'contamination' was set to 0.02. 

- [X] Explain in simple terms why anomalies might include normal activity and miss some attacks.

Anomalies might incldue normal activity and miss some attacks due to false positives and false negatives. Normal activity doesn't necessarily mean that the activity happens often/is seen often, so therefore that could be a false positive, meaning that the activity is flagged as an attack. An isolation forest is meant to flag anything that seems unusual, so if normal activity doesn't happen often enough, it can be considered unusual. In a similar fashion, an attack that looks common, the isolation forest might not flag it, leading to a false negative.

## Week 3 - Explain and submit

- [X] Record accuracy, precision, recall, F1 and the normal training-row count.

    Normal training-row count: 30,000
    Accuracy: 0.4936
    Precision: 0.8816
    Recall: 0.0926
    F1: 0.1677

- [X] Write 3-5 sentences about how your unsupervised approach compares to classification.

    The unsupervised approach of an Isolation Forest was trained using only normal training rows. A classifcation model, on the other hand,would learn from both normal and attack rows. Classification is more direct in that sense since it is trained on labeled attack rows and could learn those attack patterns. An Isolation Forest doesn't need labeled data, but makes it can misclassify some normal activity/flag it, given that the classifcation model can learn from known attacks, no matter how unusual the activity compared to normal traffic.

- [X] Commit your files and `results/p4.csv`.

## Your notes

Normal training rows used: 30,0000
#accuracy - how many predictions were correct
#precision - when flagged, how often it was actually an attack
#recall - from all the actual attacks, how many were detected
#f1 - balance of precision and recall

Normal training rows used: 30,0000

contamination = 0.02
  "accuracy": 0.4936,
  "precision": 0.8816,
  "recall": 0.0926,
  "f1": 0.1677,
  "training_data": "UNSW_NB15",

contamination = 0.01
  "accuracy": 0.4588,
  "precision": 0.7939,
  "recall": 0.0229,
  "f1": 0.0446,
  "training_data": "UNSW_NB15"


contamination = 0.05 
  "accuracy": 0.5592,
  "precision": 0.8468,
  "recall": 0.2435,
  "f1": 0.3783,
  "training_data": "UNSW_NB15"



Normal training rows used: 50,000

contamination = 0.02
  "accuracy": 0.4935,
  "precision": 0.8841,
  "recall": 0.0922,
  "f1": 0.167,
  "training_data": "UNSW_NB15"

contamination = 0.01
  "accuracy": 0.4516,
  "precision": 0.6504,
  "recall": 0.0085,
  "f1": 0.0169,
  "training_data": "UNSW_NB15"

contamnation = 0.05
  "accuracy": 0.5623,
  "precision": 0.8481,
  "recall": 0.2498,
  "f1": 0.386,
  "training_data": "UNSW_NB15"


Normal training rows used: 10,000
contamination = 0.02
  "accuracy": 0.5127,
  "precision": 0.9101,
  "recall": 0.1275,
  "f1": 0.2236,
  "training_data": "UNSW_NB15"

contamination = 0.01
  "accuracy": 0.4632,
  "precision": 0.8666,
  "recall": 0.0297,
  "f1": 0.0574,
  "training_data": "UNSW_NB15"

contamination = 0.05
  "accuracy": 0.5676,
  "precision": 0.8534,
  "recall": 0.2593,
  "f1": 0.3978,
  "training_data": "UNSW_NB15"

What I learned: 
I tested the Isolation Forest model with three different training row sizes, as well as three different contamination values. I was able to learn that the contamination value was a way of deciding how strict I wanted the model to be in terms of identifying unusual activity. The lower the contamination value, the stricter the model. 

The contamination value of 0.01 proved to be too selective since the contamination value tells the model how many anomalies to expect. It had a low recall score across all three training row sizes, meaning it failed to detect many of the actual attacks.  The contamination value of 0.05 did perform the best across all of the three training sizes. The trianing size of 10,000 also performed the best for each of the contamination values. However, the original baseline was contamination of 0.02 and training rows of 30,000. Those are the final values I chose as to not change the model solely based on test results. A few good eveualtion metrics doesn't necessarily mean "better" for an unbiased model. Sticking to what looks the best could also make the model overfit to the test set.

Going to back to why anomalies might include normal activity and miss some attacks, normal activity can be rare and therefore considered unusual and flagged as an attack. This can be seen with how recall increased from the baseline of 0.02 contamination with 0.0926 to 0.2435 with contamination = 0.05, but precision decreased from 0.8816 to 0.8468 with 30,000 rows. Based on this, a higher contamination value is expected to flag more, but that can also mean a possible increase in falsely detecting normal activity as an attack (false positive).

`contamination` is a modeling assumption. Do not pick it based on test-set labels if claiming an unbiased final test evaluation.
