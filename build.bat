@echo off
echo ============================================
echo CamoAgent Build Script
echo ============================================
echo.

echo [1/4] Installing dependencies...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Installing PyInstaller...
python -m pip install pyinstaller
if %errorlevel% neq 0 (
    echo Failed to install PyInstaller
    pause
    exit /b 1
)

echo.
echo [3/4] Building executable...
python -m PyInstaller camoagent.spec --clean
if %errorlevel% neq 0 (
    echo Build failed
    pause
    exit /b 1
)

echo.
echo [4/4] Cleaning up...
if exist build rmdir /s /q build
echo.

echo ============================================
echo Build completed successfully!
echo ============================================
echo.
echo Output location: dist\CamoAgent\
echo.
echo To run the application:
echo   dist\CamoAgent\CamoAgent.exe
echo.
pause
