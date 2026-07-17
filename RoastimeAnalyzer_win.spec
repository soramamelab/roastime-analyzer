# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_data_files

datas = [('app.py', '.')]
binaries = []
hiddenimports = [
    'streamlit.web.cli',
    'streamlit.runtime.scriptrunner',
    'streamlit.runtime.scriptrunner.script_runner',
    'pkg_resources.extern',
]

for pkg in ('streamlit', 'plotly', 'pandas', 'statsmodels', 'openpyxl', 'altair'):
    try:
        tmp = collect_all(pkg)
        datas += tmp[0]; binaries += tmp[1]; hiddenimports += tmp[2]
    except Exception:
        pass

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RoastimeAnalyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='icon.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RoastimeAnalyzer',
)
