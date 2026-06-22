[Setup]
AppId={{B5A3F1E2-7C4D-4E8A-9F2B-1A3C5D7E9F0B}
AppName=RoastimeAnalyzer
AppVersion=1.0.0
AppVerName=RoastimeAnalyzer 1.0.0
AppPublisher=Kuriya Coffee Roasters
DefaultDirName={autopf}\RoastimeAnalyzer
DefaultGroupName=RoastimeAnalyzer
OutputDir=dist
OutputBaseFilename=RoastimeAnalyzer_Setup_1.0.0
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayName=RoastimeAnalyzer
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\RoastimeAnalyzer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\RoastimeAnalyzer"; Filename: "{app}\RoastimeAnalyzer.exe"
Name: "{group}\{cm:UninstallProgram,RoastimeAnalyzer}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\RoastimeAnalyzer"; Filename: "{app}\RoastimeAnalyzer.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\RoastimeAnalyzer.exe"; Description: "{cm:LaunchProgram,RoastimeAnalyzer}"; Flags: nowait postinstall skipifsilent
