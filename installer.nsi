; ShopeeAgent NSIS Installer Script
; Build with: makensis installer.nsi

!include "MUI2.nsh"

; General Settings
Name "ShopeeAgent"
OutFile "ShopeeAgent-Setup.exe"
InstallDir "$PROGRAMFILES\ShopeeAgent"
InstallDirRegKey HKLM "Software\ShopeeAgent" "Install_Dir"
RequestExecutionLevel admin

; Version Info
VIProductVersion "1.0.0.0"
VIAddVersionKey "ProductName" "ShopeeAgent"
VIAddVersionKey "CompanyName" "ShopeeAgent"
VIAddVersionKey "LegalCopyright" "Copyright 2025"
VIAddVersionKey "FileDescription" "ShopeeAgent - AI Shopee Manager"
VIAddVersionKey "FileVersion" "1.0.0"
VIAddVersionKey "ProductVersion" "1.0.0"

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

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
    FileOpen $0 "$INSTDIR\.env.example" w
    FileWrite $0 "SUMOPOD_API_KEY=your_api_key_here$\r$\n"
    FileWrite $0 "OPENAI_API_KEY=your_openai_api_key_here$\r$\n"
    FileClose $0
    
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
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent" "DisplayVersion" "1.0.0"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ShopeeAgent" "DisplayIcon" "$INSTDIR\ShopeeAgent.exe"
    
    ; Write install directory
    WriteRegStr HKLM "Software\ShopeeAgent" "Install_Dir" "$INSTDIR"
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
