# Person 5 - Streamlit dashboard and model comparison

**Your job in plain English:** Make a simple webpage where the group can see how all four models perform. You do not need to train any model or wait for teammates to create predictions. The `demo/` folder already contains tiny **fake** prediction CSVs for you to practice with.

## Start here

```powershell
streamlit run person5_dashboard/app.py
```

A local browser tab should open. Choose **Example data (practice)** first. Once teammates upload real `results/p1.csv` ... `p4.csv`, change to **Actual model results**. The app safely skips missing files.

## Week 1 - Build the page

- [ ] Run the app with demo files.
- [ ] Read `app.py` to see how it opens the CSV files.
- [ ] Add a short introduction or change the layout in your assigned folder.

## Week 2 - Show useful comparisons

- [ ] Confirm accuracy, precision, recall and F1 display correctly.
- [ ] Customize the bar chart or add a confusion matrix as extra work.
- [ ] Check the dashboard handles one missing model file without crashing.

## Week 3 - Combine finished work

- [ ] Choose **Actual model results** after `results/p1.csv` ... `p4.csv` start arriving.
- [ ] Verify `python scripts/validate_results.py` succeeds from the root folder.
- [ ] Capture a screenshot and write 3-5 sentences comparing the available models.
- [ ] Commit your app, screenshots (if any), and notes in your own branch.

## Your notes

Best recall: TODO

Best F1: TODO

Trade-off between missed attacks and false alarms: TODO

**Important:** The demo CSVs are fabricated and never count as research results. Comparisons require exactly matching test rows and original labels.
