# ShopeeAgent Installer Guide

Panduan lengkap untuk membungkus ShopeeAgent menjadi installer yang mudah didistribusikan ke end user.

## Prerequisites

1. Python 3.10+ terinstall
2. Git (untuk cloning)
3. Windows 10/11

## Step 1: Build Executable

### Opsi A: Using build script (Recommended)

```batch
# Clone atau download project
git clone <repo-url>
cd camoagent

# Buat file .env dengan API key
echo SUMOPOD_API_KEY=your_api_key_here > .env

# Jalankan build
build.bat
```

### Opsi B: Manual Build

```bash
# Install dependencies
pip install -r requirements.txt

# Install PyInstaller
pip install pyinstaller

# Build
pyinstaller shopeeagent.spec --clean

# Output di folder dist/ShopeeAgent/
```

## Step 2: Pilihan Installer

### Option 1: NSIS (Recommended - Free)

NSIS adalah installer generator gratis yang populer untuk Windows.

#### Install NSIS
1. Download dari https://nsis.sourceforge.io/
2. Install NSIS

#### Buat installer script (installer.nsi)

```nsis
!include "MUI2.nsh"

Name "ShopeeAgent"
OutFile "ShopeeAgent-Setup.exe"
InstallDir "$PROGRAMFILES\ShopeeAgent"
InstallDirRegKey HKLM "Software\ShopeeAgent" "Install_Dir"

Section "Install"
    SetOutPath "$INSTDIR"
    
    ; Copy semua files dari dist/ShopeeAgent
    File /r "dist\ShopeeAgent\*.*"
    
    ; Buat shortcuts
    CreateDirectory "$SMPROGRAMS\ShopeeAgent"
    CreateShortCut "$SMPROGRAMS\ShopeeAgent\ShopeeAgent.lnk" "$INSTDIR\ShopeeAgent.exe"
    CreateShortCut "$DESKTOP\ShopeeAgent.lnk" "$INSTDIR\ShopeeAgent.exe"
    
    ; Buat uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Registry entries untuk Add/Remove Programs
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent" "DisplayName" "ShopeeAgent"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent" "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent" "Publisher" "ShopeeAgent"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent" "DisplayVersion" "1.0.0"
SectionEnd

Section "Uninstall"
    ; Hapus files
    RMDir /r "$INSTDIR"
    
    ; Hapus shortcuts
    Delete "$SMPROGRAMS\ShopeeAgent\*.*"
    RMDir "$SMPROGRAMS\ShopeeAgent"
    Delete "$DESKTOP\ShopeeAgent.lnk"
    
    ; Hapus registry entries
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent"
SectionEnd
```

#### Build Installer
```batch
makensis installer.nsi
```

### Option 2: Inno Setup (Free - User Friendly)

Inno Setup adalah installer generator gratis dengan UI yang lebih modern.

#### Install Inno Setup
1. Download dari https://jrsoftware.org/isinfo.php
2. Install Inno Setup

#### Buat script (installer.iss)

```iss
[Setup]
AppName=ShopeeAgent
AppVersion=1.0.0
AppPublisher=ShopeeAgent
DefaultDirName={autopf}\ShopeeAgent
DefaultGroupName=ShopeeAgent
OutputBaseFilename=ShopeeAgent-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\ShopeeAgent\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\ShopeeAgent"; Filename: "{app}\ShopeeAgent.exe"
Name: "{commondesktop}\ShopeeAgent"; Filename: "{app}\ShopeeAgent.exe"

[Run]
Filename: "{app}\ShopeeAgent.exe"; Description: "Launch ShopeeAgent"; Flags: nowait postinstall skipifsilent
```

#### Build Installer
```batch
iscc installer.iss
```

### Option 3: WiX Toolset (Professional - Enterprise)

WiX adalah installer framework untuk enterprise deployment.

#### Install WiX
```batch
winget install WiXToolset.WiX
```

#### Buat installer (installer.wxs)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
    <Product Id="*" Name="ShopeeAgent" Language="1033" Version="1.0.0.0" Manufacturer="ShopeeAgent" UpgradeCode="PUT-GUID-HERE">
        <Package InstallerVersion="200" Compressed="yes" InstallScope="perMachine" />
        <MajorUpgrade DowngradeErrorMessage="A newer version of [ProductName] is already installed." />
        <MediaTemplate EmbedCab="yes" />
        
        <Feature Id="ProductFeature" Title="ShopeeAgent" Level="1">
            <ComponentGroupRef Id="ProductComponents" />
        </Feature>
        
        <StandardDirectory Id="ProgramFilesFolder">
            <Directory Id="INSTALLFOLDER" Name="ShopeeAgent" />
        </StandardDirectory>
        
        <StandardDirectory Id="DesktopFolder" />
        
        <ComponentGroup Id="ProductComponents" Directory="INSTALLFOLDER">
            <Component Id="MainExecutable">
                <File Id="ShopeeAgentExe" Source="dist\ShopeeAgent\ShopeeAgent.exe" KeyPath="yes" />
            </Component>
        </ComponentGroup>
        
        <Icon Id="ShopeeAgentIcon" SourceFile="dist\ShopeeAgent\ShopeeAgent.exe" />
        <Property Id="ARPPRODUCTICON" Value="ShopeeAgentIcon" />
    </Product>
</Wix>
```

#### Build Installer
```batch
candle.exe installer.wxs
lux.exe installer.wixobj
```

## Step 3: Distribute

### Untuk Portable Distribution

Jika tidak ingin membuat installer, cukup zip folder `dist\ShopeeAgent`:

```batch
cd dist
powershell Compress-Archive -Path "ShopeeAgent" -DestinationPath "ShopeeAgent-Portable.zip"
```

User cukup extract dan jalankan `ShopeeAgent.exe`.

### Distribution Checklist

1. ✅ Build executable
2. ✅ Buat installer atau portable zip
3. ✅ Test di clean Windows VM
4. ✅ Buat release notes
5. ✅ Upload ke GitHub Releases / Cloud Storage

## Troubleshooting

### Build Issues

**Q: PyInstaller error "missing module"**
```bash
# Install missing module
pip install <missing-module>
# Rebuild
pyinstaller shopeeagent.spec --clean
```

**Q: Camoufox browser not found**
```bash
# Re-fetch Camoufox
python -m camoufox fetch
```

### Runtime Issues

**Q: Application crash on startup**
- Pastikan Visual C++ Redistributables terinstall
- Check log files di AppData

**Q: Browser tidak terbuka**
- Pastikan Camoufox terinstall: `python -m camoufox fetch`

## Automated Build Script

Gunakan script berikut untuk build + create installer otomatis:

```batch
@echo off
echo Building ShopeeAgent...

REM Step 1: Build
call build.bat

REM Step 2: Create NSIS installer (if NSIS installed)
where makensis >nul 2>&1
if %errorlevel% equ 0 (
    echo Creating installer...
    makensis installer.nsi
) else (
    echo NSIS not found, skipping installer...
    echo Creating ZIP instead...
    powershell Compress-Archive -Path "dist\ShopeeAgent" -DestinationPath "dist\ShopeeAgent-Portable.zip"
)

echo Done!
pause
```
