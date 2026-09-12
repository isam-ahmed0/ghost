;-------------------------------------------------------------------------------
; Ghost Qt GUI - NSIS ONLINE installer
; Compile with: makensis.exe installer\ghost-online.nsi
;
; Downloads from GitHub Releases using Windows URLDownloadToFile API.
; No external tools required (no curl, no PowerShell .bat files).
;-------------------------------------------------------------------------------

!include "MUI2.nsh"
!include "LogicLib.nsh"

!define APP_NAME      "Ghost"
!define APP_SHORT     "Ghost"
!define COMPANY       "Ghost"
!ifndef VERSION
  !define VERSION     "4.3.0"
!endif
!define VERSION_DOT   "${VERSION}.0.0"

!ifndef ROOT
  !define ROOT "${__FILEDIR__}\.."
!endif
!define SRC_ICON      "${ROOT}\data\icon.ico"

!define DOWNLOAD_URL  "https://github.com/ghostselfbot/ghost/releases/download/${VERSION}/Ghost-Windows.zip"

Name    "${APP_NAME}"
OutFile "${ROOT}\dist\Ghost-Setup.exe"

InstallDir "$LOCALAPPDATA\Programs\${APP_NAME}"
InstallDirRegKey HKCU "Software\${APP_NAME}" "Install_Location"

RequestExecutionLevel user
Unicode True
SetCompressor /SOLID lzma

Icon    "${SRC_ICON}"
UninstallIcon "${SRC_ICON}"

BrandingText "Ghost Installer"

VIProductVersion "${VERSION_DOT}"
VIAddVersionKey "ProductName"     "${APP_NAME}"
VIAddVersionKey "FileDescription" "${APP_NAME} ${VERSION} (Online)"
VIAddVersionKey "FileVersion"     "${VERSION_DOT}"
VIAddVersionKey "ProductVersion"  "${VERSION}"
VIAddVersionKey "CompanyName"     "${COMPANY}"
VIAddVersionKey "LegalCopyright"  "Copyright (c) 2026 ${COMPANY}"

;------------------------------- Modern UI 2 -------------------------------
!define MUI_ABORTWARNING
!define MUI_ICON   "${SRC_ICON}"
!define MUI_UNICON "${SRC_ICON}"

!define MUI_WELCOMEPAGE_TITLE "Welcome"
!define MUI_WELCOMEPAGE_TEXT "Ghost is a Discord selfbot toolkit with sniper, auto-reply, rich presence, and more.$\r$\n$\r$\nThis installer will download Ghost v${VERSION} from the internet."

!define MUI_FINISHPAGE_TITLE "Done"
!define MUI_FINISHPAGE_TEXT "Ghost has been installed successfully."
!define MUI_FINISHPAGE_RUN "$INSTDIR\Ghost.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Launch Ghost now"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

Function .onInit
  InitPluginsDir
  CreateDirectory "$PLUGINSDIR"
FunctionEnd

;------------------------------- Components --------------------------------
Section "Ghost Qt GUI (required)" SecMain
  SectionIn RO

  ; --- Download via Windows API ---
  DetailPrint "Downloading Ghost from GitHub..."
  DetailPrint "URL: ${DOWNLOAD_URL}"
  DetailPrint "This may take a few minutes..."

  ; Force TLS 1.2 before download
  System::Call 'wininet::InternetSetOption(0, 11, 0, 0) i'

  ; URLDownloadToFile - handles HTTPS + redirects natively
  System::Call 'urlmon::URLDownloadToFile(0, t"${DOWNLOAD_URL}", t"$PLUGINSDIR\Ghost-Windows.zip", i0, i0) i .r0'

  ${If} $0 != "0"
    MessageBox MB_ICONSTOP "Download failed (error $0). Please check your internet connection and try again."
    Quit
  ${EndIf}

  ; Verify download
  IfFileExists "$PLUGINSDIR\Ghost-Windows.zip" 0 download_failed
    Goto download_ok
  download_failed:
    MessageBox MB_ICONSTOP "Download failed. The file was not created."
    Quit
  download_ok:
  DetailPrint "Download complete."

  ; --- Extract via PowerShell (built-in) ---
  DetailPrint "Extracting files..."
  CreateDirectory "$PLUGINSDIR\extracted"

  FileOpen $0 "$PLUGINSDIR\_extract.ps1" w
  FileWrite $0 'Expand-Archive -Path "$PLUGINSDIR\Ghost-Windows.zip" -DestinationPath "$PLUGINSDIR\extracted" -Force$\r$\n'
  FileClose $0

  nsExec::ExecToStack 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$PLUGINSDIR\_extract.ps1"'
  Pop $0
  ${If} $0 != "0"
    MessageBox MB_ICONSTOP "Extraction failed. Please try again."
    Quit
  ${EndIf}
  DetailPrint "Extraction complete."

  ; --- Copy Ghost files ---
  DetailPrint "Installing Ghost..."
  SetOutPath "$INSTDIR"
  nsExec::ExecToStack 'cmd /c xcopy /E /Y "$PLUGINSDIR\extracted\Ghost\*" "$INSTDIR\"'
  Pop $0

  WriteUninstaller "$INSTDIR\Uninstall.exe"

  CreateDirectory "$SMPROGRAMS\${APP_SHORT}"
  CreateShortcut "$SMPROGRAMS\${APP_SHORT}\${APP_SHORT}.lnk" "$INSTDIR\Ghost.exe"
  CreateShortcut "$SMPROGRAMS\${APP_SHORT}\Uninstall ${APP_SHORT}.lnk" "$INSTDIR\Uninstall.exe"

  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName"     "${APP_NAME} ${VERSION}"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion"  "${VERSION}"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher"       "${COMPANY}"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayIcon"     "$INSTDIR\icon.ico"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "InstallLocation" "$INSTDIR"
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1

  WriteRegStr HKCU "Software\${APP_NAME}" "Install_Location" "$INSTDIR"
SectionEnd

Section /o "Desktop shortcut" SecDesktop
  CreateShortcut "$DESKTOP\${APP_SHORT}.lnk" "$INSTDIR\Ghost.exe"
SectionEnd

;------------------------------- Component descriptions --------------------
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecMain}    "Core Ghost files (required). Downloaded from the internet."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} "Create a shortcut on your Desktop."
!insertmacro MUI_FUNCTION_DESCRIPTION_END

;------------------------------- Uninstall --------------------------------
Section "Uninstall"
  Delete "$SMPROGRAMS\${APP_SHORT}\${APP_SHORT}.lnk"
  Delete "$SMPROGRAMS\${APP_SHORT}\Uninstall ${APP_SHORT}.lnk"
  RMDir  "$SMPROGRAMS\${APP_SHORT}"

  Delete "$DESKTOP\${APP_SHORT}.lnk"

  RMDir  /r "$INSTDIR"

  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
  DeleteRegKey HKCU "Software\${APP_NAME}"
SectionEnd
