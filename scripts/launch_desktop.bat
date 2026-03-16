@echo off
REM Composer Studio Desktop Launcher
REM Starts backend, waits for readiness, then launches the Tauri app.
REM Run from project root: scripts\launch_desktop.bat

set ROOT=%~dp0..
cd /d "%ROOT%"

echo Starting Composer Studio backend...
start /B py backend\run_server.py > nul 2>&1

echo Waiting for backend (port 8765)...
timeout /t 3 /nobreak > nul

REM Launch the built Tauri app
set EXE=src-tauri\target\release\Composer Studio.exe
if exist "%EXE%" (
    echo Launching Composer Studio...
    start "" "%EXE%"
) else (
    echo Build the app first: npm run tauri:build
    echo Expected: %EXE%
    pause
)
