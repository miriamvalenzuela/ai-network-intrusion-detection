# Windows PowerShell: first-time checklist

This is for a teammate who is opening the project for the first time.

## A. Check tools

Open PowerShell or the VS Code terminal:

```powershell
git --version
py -3.11 --version
```

If Python 3.11 is not installed but 3.12 is, use `py -3.12` below. Download Git from https://git-scm.com/ and Python from https://www.python.org/downloads/ if needed.

## B. Get the repo

On GitHub, open the repo, click **Code > HTTPS**, and copy its URL:

```powershell
cd $HOME\Documents
git clone PASTE_YOUR_GITHUB_REPOSITORY_URL_HERE
cd YOUR_REPO_FOLDER
code .
```

If `code .` is not recognized, open VS Code manually and use **File > Open Folder**. You must `cd` to the folder containing `requirements.txt` before running any Python commands.

> Only the repo owner adds the ZIP once. If this README is already on GitHub, the other teammates do not unzip or re-add anything.

## C. Set up your local Python environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/check_setup.py
```

If the activate command is blocked:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

In VS Code use **Ctrl+Shift+P > Python: Select Interpreter** and choose `.venv\Scripts\python.exe`.

## D. Make sure code runs (no real data needed)

```powershell
python scripts/generate_sample_data.py
python person1_baseline/train.py --data-dir data/sample
python scripts/validate_results.py --results-dir scratch/sample_results
```

You should see a new `scratch/sample_results/p1.csv`. This is not for the final report and is ignored by Git. Replace the person1 command with your own model command if you are Person 2, 3 or 4.

Person 5 can run the dashboard immediately:

```powershell
streamlit run person5_dashboard/app.py
```

Open the localhost link printed in PowerShell and select **Example data (practice)**.

## E. Download real prepared UNSW data and start work

```powershell
python scripts/download_dataset.py
python scripts/check_setup.py
```

If automated download fails, see `data/README.md` for manual links. Then open your person's README and follow the real dataset command. Keep CSV files in `data/raw/`, not inside person folders.

## F. Commit to GitHub (when you finish a small piece)

```powershell
git status
git switch -c person1-baseline
git add person1_baseline/
git commit -m "Add baseline dataset exploration"
git push -u origin person1-baseline
```

Replace `person1-baseline` and `person1_baseline/` with your own branch/folder. This branch command is only for the **first** time you create that branch; on future days simply run `git switch person1-baseline`. If you have a `results/p1.csv`, add it with `git add results/p1.csv` before committing.

On GitHub open a pull request into `main`. After it is merged, update your machine with `git switch main` and `git pull origin main`.
