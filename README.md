# IIMRR

IIMRR extracts a requested annual-report section into a new PDF without rasterizing or re-rendering pages. It tries bookmarks/hyperlinks, then structural Table-of-Contents heuristics, and only then an optional OpenAI-compatible free-model endpoint.

## Usage

```powershell
pip install -e .
iimrr extract report.pdf mdna -o mdna.pdf
```

Use `iimrr sections` to list supported canonical section keys. Set `IIMRR_LLM_ENDPOINT`, `IIMRR_LLM_API_KEY`, and optionally `IIMRR_LLM_MODEL` only to enable the Tier 2 fallback.

## Desktop UI

After installation, launch the simple Windows desktop interface with:

```powershell
iimrr-ui
```

If your virtual environment was created without setuptools and cannot refresh the command-line launcher, use this equivalent command from the project folder:

```powershell
.\.venv\Scripts\python.exe launch_ui.py
```

It provides PDF and output-folder browsers, an editable suggested filename, live step updates, and per-session LLM endpoint/key/model inputs.

The output preserves original PDF page content; a newly written PDF file cannot generally be byte-for-byte identical to the source container.

`-o` accepts either a destination PDF filename or an existing output directory. With a directory, IIMRR writes `<source-name>_<section>.pdf` there.
