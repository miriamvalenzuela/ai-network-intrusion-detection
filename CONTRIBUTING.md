# How to work independently without conflicting commits

The repo owner first installs and merges the starter kit. All teammates then pull it to their computers.

## One-time repo owner setup

1. Clone the existing repo (the one already containing the three-week plan PDF and Markdown).
2. Download `Network_Intrusion_Starter_Kit.zip` and extract **its contents** into the root of the cloned repo, not into another nested folder. This starter contains no `.git/` folder.
3. Verify the existing PDF/Markdown are still there. Run `git status` and confirm **no `data/raw/*.csv` or `.venv/` appears**.
4. Run a sample smoke test. Then:

   ```powershell
   git switch -c setup-starter
   git add .
   git commit -m "Add five-person intrusion detection starter structure"
   git push -u origin setup-starter
   ```

5. Make a pull request into `main` and merge it. If the maintainer is working alone on setup, pushing to `main` is possible, but using a PR is a safer habit.

## Every teammate: own folder, own branch

| Person | Branch suggestion | Only edit | Final prediction |
|---|---|---|---|
| 1 | `person1-baseline` | `person1_baseline/` | `results/p1.csv` |
| 2 | `person2-random-forest` | `person2_random_forest/` | `results/p2.csv` |
| 3 | `person3-svm` | `person3_svm/` | `results/p3.csv` |
| 4 | `person4-isolation-forest` | `person4_isolation_forest/` | `results/p4.csv` |
| 5 | `person5-dashboard` | `person5_dashboard/` | dashboard and demo screenshots |

**Important:** No one edits `project_utils/core.py`, `requirements.txt`, or `README.md` during their normal task. They are already in place. If a real change is needed, ask the group and have one owner update them in a separate small PR.

From a clean local `main` branch:

```powershell
git switch main
git pull origin main
git switch -c person2-random-forest
```

Then make changes in your own folder. Stage only your specific files:

```powershell
git status
git add person2_random_forest/
git add results/p2.csv
git commit -m "Train Random Forest and export test predictions"
git push -u origin person2-random-forest
```

Create a Pull Request to `main` on GitHub. If the CSV is not ready, skip `git add results/p2.csv` and commit the script first. Other people can keep working.

## Weekly updates in the group chat

Copy/paste this quick template (no meeting needed):

```text
Person: __
Done: __
Next: __
Blocked: none / __
Latest GitHub branch or PR: __
```

## Before merging a pull request

- [ ] Code runs from the repo root with your README command.
- [ ] Your script uses the supplied **training** data to fit and the untouched **testing** data for predictions.
- [ ] You do not use `id`, `label`, or `attack_cat` as model inputs.
- [ ] For model people: your official `results/pN.csv` has three columns and 82,332 rows.
- [ ] `python scripts/validate_results.py` passes for the results that are present.
- [ ] No large dataset CSVs, `.venv/`, or secrets appear in `git status`.
- [ ] You documented any experiments, training subset size, and warnings in your README.

If someone is behind, Person 5 keeps working with demo CSVs and then loads the missing real CSV later. This is the only final-week handoff.
