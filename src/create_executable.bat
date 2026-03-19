@echo off
echo Batch file started.

REM Set project root to the directory where this batch file is located
set "ROOT=%~dp0"
REM Remove trailing backslash if present
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"
echo ROOT is set to: %ROOT%

REM Check for pyinstaller (but don't exit if not found)
echo Checking for PyInstaller...
where pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Warning: PyInstaller not found in PATH.
    echo You may need to activate your Python environment or install pyinstaller (pip install pyinstaller)
    echo Continuing anyway...
) else (
    echo PyInstaller found.
)

echo About to call pyinstaller...
pyinstaller --noconfirm --windowed --onefile^
    --icon "%ROOT%\icon.ico" ^
    --version-file "%ROOT%\version.txt" ^
    "%ROOT%\main.py"

if errorlevel 1 (
    echo PyInstaller failed to run.
) else (
    echo PyInstaller command finished successfully.
)
echo Done. Check the "dist" folder for the generated executable.
pause


if errorlevel 1 (
    echo PyInstaller failed to run.
) else (
    echo PyInstaller command finished successfully.
)
echo Done. Check the "dist" folder for the generated executable.
pause
cmd /k