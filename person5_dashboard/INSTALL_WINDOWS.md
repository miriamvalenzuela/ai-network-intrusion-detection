# Install this dashboard refresh

1. In VS Code / PowerShell, open your cloned repository and ensure `git branch --show-current` shows `person5-dashboard`.
2. **Commit any current edits** to `person5_dashboard/` first, because extracting this ZIP replaces its existing `app.py`, styling, and helper files.
3. Download `Network_Intrusion_Dashboard_Gridle_Style.zip` into your Windows Downloads folder.
4. From the repository root, run:

```powershell
Expand-Archive -Path "$HOME\Downloads\Network_Intrusion_Dashboard_Gridle_Style.zip" -DestinationPath . -Force
```

5. Activate your environment (if needed), run the unit tests, then launch:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest discover -s person5_dashboard/tests -v
streamlit run person5_dashboard/app.py
```

6. Check the **Overview**, **Model details**, and **How it works** pages in both **Light** and **Dark** modes. Start with Guided demo; switch to Team results if your classmates' CSVs are available.
7. When you're satisfied:

```powershell
git status
git add person5_dashboard/
git commit -m "Refresh dashboard layout and add theme toggle"
git push
```

**What's replaced:** Only the supplied files under `person5_dashboard/`. Your existing `demo/` CSVs, teammates' model folders, and root `results/` CSVs are not included in this update.

**If the old page persists:** Stop Streamlit with `Ctrl+C`, restart the app, and hard refresh the browser (`Ctrl+F5`).
