@echo off
echo ============================================================
echo  GitHub Project setup - Hospital Appointment + RAG Chat
echo ============================================================
echo.
echo You need a Personal Access Token WITH "project" scope:
echo   https://github.com/settings/tokens
echo   - Generate new token (classic)
echo   - Check: repo + project
echo.
set /p GITHUB_TOKEN=Paste token here and press Enter: 
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\setup-github-project.ps1"
echo.
pause
