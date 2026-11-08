# Dataset: prepared UNSW-NB15 training and testing CSVs

Use the **prepared split**, not the much larger four-part raw capture dataset.

Official dataset description and academic citation/terms:
https://research.unsw.edu.au/projects/unsw-nb15-dataset

Download source (public mirror of the prepared files):
https://huggingface.co/datasets/Mouwiya/UNSW-NB15-small/tree/main

Optional: from repo root run `python scripts/download_dataset.py` after installing requirements.

Place the two files here, without changing their names:

```text
data/raw/UNSW_NB15_training-set.csv  (175,341 data rows)
data/raw/UNSW_NB15_testing-set.csv   (82,332 data rows)
```

These files are **NOT** in GitHub: the `.gitignore` intentionally excludes them. Every teammate downloads their own copy. `label` means 0=normal or 1=attack. `attack_cat` contains an attack category; like `label` and `id`, it must **not** be used as a model input (otherwise predictions can be misleading due to label leakage).

The file `data/sample/` is for generated synthetic training/testing data to check setup. It is not evidence for the class report; never compare synthetic scores to real dataset scores.

Use only the training CSV for learning encoders, scalers, and classifier parameters. Keep the original test file order unchanged for comparisons. The datasets describe historical/synthetic traffic from the original UNSW research environment; they do not measure live threat detection.

If you publish research or coursework based on UNSW-NB15, cite the originators as instructed by the official UNSW page. Primary paper: Moustafa, N., & Slay, J. (2015). UNSW-NB15: A comprehensive data set for network intrusion detection systems. MilCIS 2015.
