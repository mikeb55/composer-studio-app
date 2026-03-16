# Composer Studio — Windows Desktop Packaging Guide

This guide explains how to build and launch Composer Studio as a Windows desktop app.

---

## Prerequisites

- **Node.js** (v18+)
- **Python** (3.9+) with `uvicorn`, `fastapi`, and backend dependencies
- **Rust** (for Tauri build) — install from [rustup.rs](https://rustup.rs); Windows also needs Visual Studio Build Tools (C++ workload)
- **creative-engines** — sibling repo at `../creative-engines` or set `CREATIVE_ENGINES_PATH` env var

---

## Build the Desktop App

1. Install dependencies:
   ```bash
   npm install
   py -m pip install -r backend/requirements.txt
   ```

2. Build the Tauri app:
   ```bash
   npm run tauri:build
   ```

3. Build output:
   - **Executable:** `src-tauri/target/release/Composer Studio.exe`
   - **Installer (MSI):** `src-tauri/target/release/bundle/msi/Composer Studio_0.1.0_x64_en-US.msi`
   - **Installer (NSIS):** `src-tauri/target/release/bundle/nsis/Composer Studio_0.1.0_x64-setup.exe`

---

## Launch the Packaged App

The desktop app requires the **backend API** to run. Two options:

### Option A: Launcher script (recommended)

From the project root:

```bash
scripts\launch_desktop.bat
```

This starts the backend, waits for readiness, then launches the Tauri app.

### Option B: Manual

1. Start the backend in a terminal:
   ```bash
   py backend/run_server.py
   ```
2. Run the executable:
   ```bash
   src-tauri\target\release\Composer Studio.exe
   ```

---

## Desktop Shortcut

1. Right-click `Composer Studio.exe` (or the launcher script)
2. **Send to** → **Desktop (create shortcut)**
3. For the launcher: right-click the shortcut → **Properties** → set **Start in** to the project root so the backend path resolves correctly

---

## creative-engines Setup

Composer Studio needs the **creative-engines** repository locally:

- **Default path:** `C:\Users\<you>\Documents\Cursor AI Projects\creative-engines`
- **Override:** set `CREATIVE_ENGINES_PATH` to your path before starting the backend

---

## Verify the Packaged App

1. Launch the app (via launcher or manually)
2. Confirm engines load (Preset dropdown or Hybrid view)
3. Generate one piece (e.g. preset `wheeler_lyric`, input "test")
4. View notation in the score viewer
5. Export one MusicXML file

---

## Development Mode

Single-command dev (backend + frontend + Tauri window):

```bash
npm run tauri:dev
```

---

## Configuration Summary

| Item | Value |
|------|-------|
| App name | Composer Studio |
| Window size | 1200×800 (min 800×600) |
| Backend port | 8765 |
| Frontend dist | `dist/` |
| Build command | `npm run build:tauri` |

---

## Troubleshooting

- **"cargo not found"** — Install Rust via [rustup.rs](https://rustup.rs)
- **Backend connection failed** — Ensure backend is running on port 8765 before opening the app
- **No engines** — Set `CREATIVE_ENGINES_PATH` and ensure creative-engines is cloned and built
