@echo off
cd /d "%~dp0"
echo Updating database for today...
.\.venv\Scripts\python.exe app.py init-db
if errorlevel 1 (
  echo ERROR: init-db failed. Check START.md
  pause
  exit /b 1
)
echo Starting server. Open http://127.0.0.1:5000/ in browser. Press Ctrl+C to stop.
.\.venv\Scripts\python.exe app.py run
pause
