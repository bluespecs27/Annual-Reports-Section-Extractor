# Uploading IIMRR to GitHub

This folder is a clean source distribution. It deliberately excludes the local virtual environment, cached test files, generated PDFs, working data, and API keys.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
.\.venv\Scripts\python.exe launch_ui.py
```

For the command-line interface:

```powershell
iimrr extract "C:\Reports\annual-report.pdf" mdna -o "C:\Reports\mdna.pdf"
```

## Upload

Create an empty GitHub repository, then run these commands from this folder:

```powershell
git init
git add .
git commit -m "Initial IIMRR release"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Do not commit an API key. Enter it in the desktop UI for each session or set it as an environment variable on your own machine.
