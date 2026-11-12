"""Person 5: minimal Streamlit results dashboard, usable before models finish."""
from pathlib import Path
import pandas as pd
import streamlit as st
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

ROOT = Path(__file__).resolve().parents[1]
NAMES = {
    1: "Person 1 - Logistic Regression",
    2: "Person 2 - Random Forest",
    3: "Person 3 - Linear SVM",
    4: "Person 4 - Isolation Forest",
}
REQUIRED = ["row_id", "y_true", "y_pred"]

st.set_page_config(page_title="Network Intrusion Model Comparison", layout="wide")
st.title("Network Intrusion Detection - Model Comparison")
st.markdown("""
### Project Overview

This dashboard compares four machine learning models
trained to identify suspicious network traffic.

Each model predicts whether a network record represents:

- **0 - Normal Traffic**
- **1 - Potential Attack**

We compare model performance using accuracy, precision,
recall, and F1-score to understand which methods are
most effective at identifying potential threats.

**Models:** Logistic Regression, Random Forest,
Support Vector Machine, and Isolation Forest.
""")

mode = st.radio("Which results should I show?", ["Example data (practice)", "Actual model results"], horizontal=True)
if mode == "Example data (practice)":
    directory = ROOT / "person5_dashboard" / "demo"
    st.info("These are FAKE predictions for testing the dashboard. Do not use these scores in the final presentation.")
else:
    directory = ROOT / "results"
    st.caption("Real-model predictions from results/p1.csv through results/p4.csv.")

frames = {}
for number, name in NAMES.items():
    path = directory / f"p{number}.csv"
    if not path.exists():
        st.warning(f"{name}: no CSV submitted yet. That is okay - this model can be added later.")
        continue
    try:
        df = pd.read_csv(path)
        if df.columns.tolist() != REQUIRED:
            st.error(f"{path.name} must have exactly these columns: {REQUIRED}")
            continue
        if df["row_id"].tolist() != list(range(len(df))):
            st.error(f"{path.name}: row_id must start at 0 and stay in order.")
            continue
        if df[["y_true", "y_pred"]].isna().any().any() or not df["y_true"].isin([0, 1]).all() or not df["y_pred"].isin([0, 1]).all():
            st.error(f"{path.name}: both labels must be 0 or 1.")
            continue
        frames[number] = df
    except Exception as exc:
        st.error(f"Cannot read {path.name}: {exc}")

# Do not compare models evaluated on a different row order or ground truth.
if len(frames) > 1:
    reference = next(iter(frames.values()))
    bad = [number for number, df in frames.items()
           if not df[["row_id", "y_true"]].equals(reference[["row_id", "y_true"]])]
    if bad:
        st.error("Some prediction files have different row IDs or true labels. Fix them before comparing scores.")
        frames = {}

if not frames:
    st.info("No comparable model files found. Choose example data or wait for teammates to submit results.")
else:
    rows = []
    for number, df in frames.items():
        actual, predicted = df["y_true"], df["y_pred"]
        rows.append({
            "Model": NAMES[number],
            "Accuracy": accuracy_score(actual, predicted),
            "Precision": precision_score(actual, predicted, zero_division=0),
            "Recall": recall_score(actual, predicted, zero_division=0),
            "F1": f1_score(actual, predicted, zero_division=0),
        })
    metrics = pd.DataFrame(rows).set_index("Model")
    st.subheader("Model scores")
    st.dataframe(metrics.style.format("{:.3f}"), use_container_width=True)
    st.subheader("Comparison")
    st.bar_chart(metrics[["Precision", "Recall", "F1"]])
    st.subheader("Example predictions")
    selected = st.selectbox("Select a model", [NAMES[k] for k in frames])
    chosen_number = next(k for k in frames if NAMES[k] == selected)
    st.dataframe(frames[chosen_number].head(15), use_container_width=True)
    st.caption("The data is an offline research dataset, not live network monitoring.")

# TODO for Person 5: Add a confusion matrix, explain the results, and capture a screenshot.
