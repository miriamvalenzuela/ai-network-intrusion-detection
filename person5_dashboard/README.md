# Network Insights - Model Evaluation Dashboard

A Streamlit interface for **Person 5** of the AI Network Intrusion Detection final project. It compares four models using their exported binary predictions on the prepared UNSW-NB15 test set. This is an **offline evaluation dashboard**, not a live intrusion monitor.

## Start here (Windows / PowerShell)

Run all commands from the **repository root** (the folder containing `requirements.txt`):

```powershell
# If the virtual environment is not already active:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
python -m unittest discover -s person5_dashboard/tests -v
streamlit run person5_dashboard/app.py
```

Open `http://localhost:8501` if it does not open automatically. Choose **Guided demo** to test the interface without waiting for the other model owners.

## Navigating the application

| Page | Purpose |
|---|---|
| **Overview** | Evaluation cards, a selected model's outcome breakdown, model ranking, and a full scores table. |
| **Model details** | Select one model, read its confusion matrix, inspect false alarms and missed attacks, and export filtered predictions. |
| **How it works** | Explains the workflow, model types, metrics, and required data format. |

Use **Prediction source** in the sidebar to switch between practice data and team results. Use the **Dark mode** switch in the sidebar to change between the light and dark themes; the selected appearance remains active during the current Streamlit session. Light mode is the default. The interface uses native Streamlit input controls for keyboard navigation.

### Data integrity

Team results must appear at the repository root as:

```text
results/p1.csv  # Logistic Regression
results/p2.csv  # Random Forest
results/p3.csv  # Linear SVM
results/p4.csv  # Isolation Forest
```

Each CSV must have exactly these columns:

```csv
row_id,y_true,y_pred
0,0,0
1,1,1
2,1,0
```

- `row_id` follows the original testing file's **0-based position**, in increasing order.
- `y_true` is the official label: `0=normal`, `1=attack`.
- `y_pred` is that model's prediction, using the same labels.
- Real files must each contain **82,332 test rows**. All models must have matching `row_id` and `y_true` columns.
- Missing or malformed models are excluded from the comparison with a visible explanation. The app does **not** re-train or edit their files.
- The files in `person5_dashboard/demo/` are deliberately fabricated. **Never present demo scores as real model performance.**

## Code organization

| File | Responsibility |
|---|---|
| `app.py` | Streamlit pages, navigation, widgets, orchestration. |
| `dashboard_data.py` | Pure data validation, loading, metrics, comparisons. |
| `dashboard_charts.py` | Pure functions returning accessible comparison, donut, matrix, and table markup. |
| `dashboard_theme.py` | Light/dark design tokens and stylesheet loader. |
| `theme.css` | Shared layout, component styles, responsive rules, focus states. |
| `tests/` | Unit tests for data validation, visual component output, and theme tokens. |
| `demo/` | Small illustrative prediction CSVs supplied with the starter kit. |

The data layer intentionally stays separate from the UI. If you want to adjust colors, use `dashboard_theme.py`. For spacing and layout, edit `theme.css`. For text or page structure, edit `app.py`. For a score calculation, edit `dashboard_data.py` **and update the associated tests**.

Comments explain non-obvious decisions, not every line of code. The previous starter's data format and evaluation behavior are maintained.

## Run checks before committing

```powershell
python -m unittest discover -s person5_dashboard/tests -v
python scripts/validate_results.py --results-dir person5_dashboard/demo
```

The second command validates the original demo files. Once official files are submitted, run `python scripts/validate_results.py` from the repository root.

### Your Git branch

```powershell
git branch --show-current  # should be person5-dashboard
git status
git add person5_dashboard/
git commit -m "Refine dashboard design and add light dark themes"
git push
```

Use `git push -u origin person5-dashboard` if the branch has not been published yet. Stage only your folder; do not accidentally commit the virtual environment, raw datasets, or teammates' work.

## Evaluation and accessibility notes

- The model comparison uses **bar charts**, not invented time series; the source data contains categorical model scores, not temporal trends.
- The outcome donut and segmented bar show the four **mutually exclusive prediction outcomes** for one model. Counts and percentages also appear in text.
- Confusion matrices are semantic HTML tables with row/column labels, numerical counts, and row-based percentages.
- Most dynamic text is escaped before rendering. Data validation rejects incomplete test files, shuffled rows, and incompatible labels.
- Theme preferences are session-scoped. They are not written into the repo or a browser cookie.
- This is an academic demonstration; live traffic response, adversarial robustness, and production deployment are out of scope.
