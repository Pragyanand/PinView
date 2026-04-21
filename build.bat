@echo off
REM ─────────────────────────────────────────
REM  PinView – Build Script (Windows)
REM ─────────────────────────────────────────

REM Ensure script runs from its own folder
cd /d %~dp0

REM Verify Python is available
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo.
echo [1/4] Cleaning old builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q *.spec 2>nul

echo.
echo [2/4] Installing dependencies...
pip install pillow pywin32 pyinstaller

echo.
echo [3/4] Building PinView.exe...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name PinView ^
    pinview.py

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Build failed. Fix the error above.
    pause
    exit /b
)

echo.
echo [4/4] Done!
echo.

IF EXIST "dist\PinView.exe" (
    echo ✅ Build successful!
    echo Location: %CD%\dist\PinView.exe
    explorer dist
) ELSE (
    echo ❌ Build finished but EXE not found.
)

pause