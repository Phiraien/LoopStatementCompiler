@echo off
setlocal
cd /d "%~dp0"

rem Prefer the official Windows Python launcher when available.
where py >nul 2>&1
if not errorlevel 1 (
    py -3 -m gui.app
    goto :result
)

where python >nul 2>&1
if not errorlevel 1 (
    python -m gui.app
    goto :result
)

echo Python 3 was not found.
echo Install Python 3 from https://www.python.org/downloads/windows/
echo During installation, enable Tcl/Tk and optionally Add Python to PATH.
pause
exit /b 1

:result
if errorlevel 1 (
    echo.
    echo GUI exited with an error. Make sure Python 3 and Tkinter are installed.
    pause
)
