; ShopeeAgent NSIS Installer Script
; Build with: makensis installer.nsi

!include "MUI2.nsh"
!include "FileFunc.nsh"

; General Settings
Name "ShopeeAgent"
OutFile "ShopeeAgent-Setup.exe"
InstallDir "$PROGRAMFILES64\ShopeeAgent"
InstallDirRegKey HKLM "Software\ShopeeAgent" "Install_Dir"
RequestExecutionLevel admin

; Version Info
VIProductVersion "1.1.0.0"
VIAddVersionKey "ProductName" "ShopeeAgent"
VIAddVersionKey "CompanyName" "ShopeeAgent"
VIAddVersionKey "LegalCopyright" "Copyright 2025"
VIAddVersionKey "FileDescription" "ShopeeAgent - AI Shopee Manager"
VIAddVersionKey "FileVersion" "1.2.0"
VIAddVersionKey "ProductVersion" "1.2.0"

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "logoicon-removebg-preview.ico"
!define MUI_UNICON "logoicon-removebg-preview.ico"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Languages
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Indonesian"

; Installer Section
Section "Install"
    SetOutPath "$INSTDIR"
    
    ; Copy all files from dist/ShopeeAgent
    File /r "dist\ShopeeAgent\*.*"
    
    ; Create .env file with template
    FileOpen $0 "$INSTDIR\.env" w
    FileWrite $0 "SUMOPOD_API_KEY=your_api_key_here$\r$\n"
    FileWrite $0 "OPENAI_API_KEY=your_openai_api_key_here$\r$\n"
    FileWrite $0 "OPENAI_BASE_URL=https://ai.sumopod.com/v1$\r$\n"
    FileClose $0
    
    ; Create README for first-time users
    FileOpen $1 "$INSTDIR\README_FIRST.txt" w
    FileWrite $1 "=== SHOPEAGENT SETUP COMPLETE ===$\r$\n$\r$\n"
    FileWrite $1 "1. Edit .env file in this folder and add your API key:$\r$\n"
    FileWrite $1 "   SUMOPOD_API_KEY=your_key_here$\r$\n$\r$\n"
    FileWrite $1 "2. First run will download Camoufox browser (requires internet)$\r$\n$\r$\n"
    FileWrite $1 "3. If app doesn't start, run this command:$\r$\n"
    FileWrite $1 "   python -m camoufox fetch$\r$\n$\r$\n"
    FileWrite $1 "4. Check ShopeeAgent.log for error logs$\r$\n"
    FileClose $1
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Create Start Menu shortcuts
    CreateDirectory "$SMPROGRAMS\ShopeeAgent"
    CreateShortCut "$SMPROGRAMS\ShopeeAgent\ShopeeAgent.lnk" "$INSTDIR\ShopeeAgent.exe" "" "$INSTDIR\ShopeeAgent.exe" 0
    CreateShortCut "$SMPROGRAMS\ShopeeAgent\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\Uninstall.exe" 0
    
    ; Create Desktop shortcut
    CreateShortCut "$DESKTOP\ShopeeAgent.lnk" "$INSTDIR\ShopeeAgent.exe" "" "$INSTDIR\ShopeeAgent.exe" 0
    
    ; Write registry for Add/Remove Programs
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent" "DisplayName" "ShopeeAgent"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent" "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent" "Publisher" "ShopeeAgent"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent" "DisplayVersion" "1.2.0"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent" "DisplayIcon" "$INSTDIR\ShopeeAgent.exe"
    
    ; Get installed size
    ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
    IntFmt $0 "0x%08X" $0
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent" "EstimatedSize" "$0"
    
    ; Write install directory
    WriteRegStr HKLM "Software\ShopeeAgent" "Install_Dir" "$INSTDIR"
    
    ; Ask user if they want to open the README
    MessageBox MB_YESNO "Instalasi selesai!$\n$\nBuka file panduan penggunaan (README)?" IDNO skip_readme
        Exec '"$INSTDIR\ShopeeAgent-Setup-README.txt"'
    skip_readme:
SectionEnd

; Uninstaller Section
Section "Uninstall"
    ; Kill running process
    nsExec::ExecToLog 'taskkill /F /IM ShopeeAgent.exe'
    
    ; Delete files
    RMDir /r "$INSTDIR"
    
    ; Delete Start Menu shortcuts
    RMDir /r "$SMPROGRAMS\ShopeeAgent"
    
    ; Delete Desktop shortcut
    Delete "$DESKTOP\ShopeeAgent.lnk"
    
    ; Delete registry entries
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent"
    DeleteRegKey HKLM "Software\ShopeeAgent"
SectionEnd
