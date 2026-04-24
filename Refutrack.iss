[Setup]
AppName=RefuTrack
AppVersion=1.0
AppPublisher=Tu Empresa
AppPublisherURL=https://tu-sitio.com
AppSupportURL=https://tu-sitio.com/support
AppUpdatesURL=https://tu-sitio.com/updates
DefaultDirName={autopf}\RefuTrack
DefaultGroupName=RefuTrack
AllowNoIcons=yes
LicenseFile=
OutputDir=installer
OutputBaseFilename=RefuTrack-Setup
SetupIconFile=refu.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\RefuTrack.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "refu.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\RefuTrack"; Filename: "{app}\RefuTrack.exe"; IconFilename: "{app}\refu.ico"
Name: "{group}\{cm:UninstallProgram,RefuTrack}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\RefuTrack"; Filename: "{app}\RefuTrack.exe"; IconFilename: "{app}\refu.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\RefuTrack.exe"; Description: "{cm:LaunchProgram,RefuTrack}"; Flags: nowait postinstall skipifsilent
