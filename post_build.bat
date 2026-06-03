@echo off
chcp 65001 >nul
echo ============================================
echo Post-Build: Copy ALL data files
echo ============================================
echo.
echo This script copies 535+ non-Python files from
echo 7 packages that PyInstaller doesn't auto-bundle.
echo.
echo Run this AFTER every PyInstaller build.
echo.

set "DIST=dist\ShopeeAgent\_internal"
set "SITE=C:\Users\THINKPAD\AppData\Local\Programs\Python\Python311\Lib\site-packages"

echo Copying ALL non-Python files from camoufox, browserforge, apify...
for %%p in (camoufox browserforge apify_fingerprint_datapoints language_tags crewai click playwright) do (
    echo   %%p...
    robocopy "%SITE%\%%p" "%DIST%\%%p" /E /XF *.py *.pyc /NFL /NDL /NJH /NJS >nul
    echo   [OK] %%p
)

echo.
echo Copying crewai translations...
robocopy "%SITE%\crewai\translations" "%DIST%\crewai\translations" /E /NFL /NDL /NJH /NJS >nul
echo [OK] crewai/translations

echo.
echo ============================================
echo Post-build complete!
echo Now run: makensis installer.nsi
echo ============================================
pause
