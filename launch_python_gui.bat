@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if not errorlevel 1 (
    py -3 gui.py
    goto :done
)
where python >nul 2>&1
if not errorlevel 1 (
    python gui.py
    goto :done
)
echo Python 3 was not found. Install Python with Tkinter enabled.
pause
exit /b 1
:done
if errorlevel 1 pause
