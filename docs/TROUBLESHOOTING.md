# Common beginner problems

**`python` or `py` not recognized**: Install Python 3.11/3.12 from python.org and reopen PowerShell. Verify `py --version`. Install Git separately if `git` is missing.

**`ModuleNotFoundError: No module named 'pandas'` or `streamlit`**: Activate `.venv` and run `python -m pip install -r requirements.txt`. Check that VS Code selected `.venv\\Scripts\\python.exe`.

**PowerShell says scripts are disabled when activating `.venv`**: Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then `./.venv/Scripts/Activate.ps1` again. This is a per-terminal fix.

**Dataset missing**: From repo root run `python scripts/download_dataset.py` or manually save the prepared CSVs as `data/raw/UNSW_NB15_training-set.csv` and `data/raw/UNSW_NB15_testing-set.csv`. Double-check filenames and `data/README.md`.

**Dataset downloader failed or a login page appeared**: Use the manual links in `data/README.md`, save the two CSVs without renaming, and rerun the model. Some campuses or networks block file mirrors.

**Script cannot find `requirements.txt` or `project_utils`**: Your terminal is probably not in the repo root. Run `pwd` in PowerShell and `dir` to confirm you can see the root `README.md`, `requirements.txt`, and person folders.

**SVM seems slow**: Keep `--max-train-rows 30000` or try `--max-train-rows 5000` first. A convergence warning means you should investigate the solver and document it; it is not a reason to fake your results.

**Streamlit displays only example data**: Switch its radio button to `Actual model results`. Your teammates' `results/pN.csv` files must be merged into your local branch first. Run `git pull origin main` from a clean `main` branch after the PRs merge.

**Dashboard says result files don't match**: Do not shuffle the test rows. Run `python scripts/validate_results.py` and fix the reported model CSV. Every file must have identical `row_id` and `y_true` columns.

**`git push` asks for a password**: GitHub HTTPS usually authenticates with a web browser or credentials manager, not your GitHub account password. Use Git Credential Manager or GitHub CLI if prompted. Do not put tokens into repo files.

**`git add .` included huge files**: Before committing run `git status`. `.gitignore` excludes `data/raw/`, sample data, `.venv/`, and `scratch/`. If you already tracked a dataset by mistake, use `git rm --cached <path>` (removes it from staging/tracking, not from disk) and get help cleaning branch history if the file was pushed.

**Windows has no working Python 3.11**: Try `py -3.12` instead. Do not mix versions randomly within one `.venv`.
