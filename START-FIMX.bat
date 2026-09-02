@echo off
REM FIM-X production launcher.
REM Uses the project virtual environment when available.
setlocal EnableExtensions
cd /d "%~dp0"

echo.
echo ========================================
echo FIM-X 0.4.1 - Production Console
echo ========================================
echo.

if exist ".venv\Scripts\python.exe" (
    set "PY=%CD%\.venv\Scripts\python.exe"
) else (
    where py >nul 2>&1
    if not errorlevel 1 (
        set "PY=py"
    ) else (
        where python >nul 2>&1
        if errorlevel 1 (
            echo ERROR: Python was not found. Run SETUP.bat first.
            pause
            exit /b 1
        )
        set "PY=python"
    )
)

if not exist "run.py" (
    echo ERROR: run.py was not found in:
    echo %CD%
    pause
    exit /b 1
)

"%PY%" run.py %*
set "RC=%ERRORLEVEL%"

echo.
if not "%RC%"=="0" (
    echo FIM-X exited with error code %RC%.
    echo Review the message above and the FIM-X logs for details.
) else (
    echo FIM-X stopped normally.
)
pause
exit /b %RC%
