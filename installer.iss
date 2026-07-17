[Setup]
AppName=Roastime Analyzer
AppVersion=1.0.0
AppPublisher=KuriyaCoffee
AppPublisherURL=https://github.com/mkuriya4989/roastime-analyzer
DefaultDirName={autopf}\RoastimeAnalyzer
DefaultGroupName=Roastime Analyzer
UninstallDisplayIcon={app}\RoastimeAnalyzer.exe
OutputDir=installer_output
OutputBaseFilename=RoastimeAnalyzer_Setup
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
SetupIconFile=icon.ico
WizardStyle=modern

[Languages]
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\RoastimeAnalyzer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Roastime Analyzer"; Filename: "{app}\RoastimeAnalyzer.exe"
Name: "{group}\Roastime Analyzer をアンインストール"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Roastime Analyzer"; Filename: "{app}\RoastimeAnalyzer.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\RoastimeAnalyzer.exe"; Description: "Roastime Analyzer を起動"; Flags: nowait postinstall skipifsilent
