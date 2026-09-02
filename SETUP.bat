@echo off
REM FIM-X production setup for Windows.
REM Creates an isolated virtual environment and installs the pinned dependencies.
setlocal EnableExtensions
cd /d "%~dp0"

echo.
echo ========================================
echo FIM-X 0.4.1 - Production Setup
echo ========================================
echo.

where py >nul 2>&1
if not errorlevel 1 (
    set "PY=py"
) else (
    where python >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python 3.10 or newer was not found on PATH.
        echo Install Python 3.10+ and enable the launcher/PATH option.
        pause
        exit /b 1
    )
    set "PY=python"
)

%PY% -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)"
if errorlevel 1 (
    echo ERROR: FIM-X requires Python 3.10 or newer.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating isolated virtual environment...
    %PY% -m venv .venv
    if errorlevel 1 (
        echo ERROR: Could not create .venv.
        pause
        exit /b 1
    )
)

set "VPY=%CD%\.venv\Scripts\python.exe"
echo Using: %VPY%
echo.

if exist wheelhouse (
    echo Installing pinned dependencies from offline wheelhouse...
    "%VPY%" -m pip install --no-index --find-links wheelhouse -r requirements.txt
) else (
    echo Installing pinned dependencies from requirements.txt...
    echo Internet access is required when no wheelhouse is bundled.
    "%VPY%" -m pip install -r requirements.txt
)
if errorlevel 1 (
    echo.
    echo ERROR: Dependency installation failed.
    echo If this machine is offline, place the matching wheels in the wheelhouse folder.
    pause
    exit /b 1
)

echo.
echo Setup completed successfully.
echo Start FIM-X with START-FIMX.bat
pause
exit /b 0
