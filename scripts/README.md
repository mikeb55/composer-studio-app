# Composer Studio Scripts

## launch_desktop.bat

Starts the backend API and launches the packaged Composer Studio desktop app.

**Usage:** Run from project root:
```bash
scripts\launch_desktop.bat
```

**Requirements:**
- Python with backend dependencies installed
- App built via `npm run tauri:build`
- creative-engines available (set `CREATIVE_ENGINES_PATH` if needed)
