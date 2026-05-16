@echo off
setlocal EnableDelayedExpansion

echo ============================================
echo ShopeeAgent Build Script
echo ============================================
echo.

echo [1/5] Installing dependencies...
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

echo.
echo [2/5] Installing PyInstaller...
python -m pip install pyinstaller --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install PyInstaller
    pause
    exit /b 1
)
echo [OK] PyInstaller installed

echo.
echo [3/5] Installing additional build dependencies...
python -m pip install pydantic-settings --quiet
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install pydantic-settings
)
echo [OK] Build dependencies installed

echo.
echo [4/5] Building executable...
if exist "shopeeagent.spec" (
    python -m PyInstaller shopeeagent.spec --clean
) else (
    python -m PyInstaller camoagent.spec --clean --name ShopeeAgent
)
if %errorlevel% neq 0 (
    echo [ERROR] Build failed
    pause
    exit /b 1
)
echo [OK] Executable built

echo.
echo [5/5] Creating distribution folder...
if exist "dist\ShopeeAgent" rmdir /s /q "dist\ShopeeAgent"
if not exist "dist" mkdir "dist"
move /y "ShopeeAgent" "dist\" >nul 2>&1
if exist "build" rmdir /s /q "build"
if exist "ShopeeAgent.spec" del /q "ShopeeAgent.spec" 2>nul

echo.
echo ============================================
echo Build completed successfully!
echo ============================================
echo.
echo Output location: dist\ShopeeAgent\
echo.
echo To create installer, use one of:
echo   - NSIS: makensis installer.nsi
echo   - Inno Setup: iscc installer.iss
echo   - WiX: candle.exe installer.wxs
echo.
echo To run the application:
echo   dist\ShopeeAgent\ShopeeAgent.exe
echo.
pause
