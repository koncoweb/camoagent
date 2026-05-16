@echo off
echo ============================================
echo ShopeeAgent Installer Builder
echo ============================================
echo.

REM Check if NSIS is installed
where makensis >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] NSIS found
    echo.
    echo Building installer...
    makensis installer.nsi
    echo.
    echo ============================================
    echo Build complete!
    echo ============================================
    echo Installer: ShopeeAgent-Setup.exe
    echo.
    echo To distribute:
    echo   1. Share ShopeeAgent-Setup.exe
    echo   2. Or share dist\ShopeeAgent folder as ZIP
    echo.
    pause
    exit /b 0
)

echo [WARNING] NSIS is not installed.
echo.
echo Please install NSIS using one of these methods:
echo.
echo Option 1: Winget (recommended)
echo   winget install NSIS.NSIS
echo.
echo Option 2: Manual download
echo   1. Go to: https://nsis.sourceforge.io/Download.html
echo   2. Download NSIS setup file
echo   3. Install NSIS
echo.
echo Option 3: Chocolatey
echo   choco install nsis
echo.
echo After installing NSIS, run this script again.
echo.
echo ============================================
echo Creating portable ZIP as alternative...
echo ============================================
echo.

REM Create portable ZIP
powershell -Command "Compress-Archive -Path 'dist\ShopeeAgent\*' -DestinationPath 'dist\ShopeeAgent-Portable.zip' -Force"

if exist "dist\ShopeeAgent-Portable.zip" (
    echo [OK] Portable ZIP created: dist\ShopeeAgent-Portable.zip
) else (
    echo [ERROR] Failed to create ZIP
)

echo.
echo ============================================
echo Output files:
echo ============================================
echo.
if exist "dist\ShopeeAgent" (
    echo Folder: dist\ShopeeAgent\
    dir /b "dist\ShopeeAgent\ShopeeAgent.exe"
)
if exist "ShopeeAgent-Setup.exe" (
    echo Installer: ShopeeAgent-Setup.exe
)
if exist "dist\ShopeeAgent-Portable.zip" (
    echo Portable: dist\ShopeeAgent-Portable.zip
)
echo.
pause
