@echo off
setlocal
cd /d "%~dp0"
python -m gui.app
if errorlevel 1 (
    echo.
    echo GUI exited with an error. Make sure Python 3 and Tkinter are installed.
    pause
)
