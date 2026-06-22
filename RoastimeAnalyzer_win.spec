# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_data_files

datas = [('app.py', '.')]
binaries = []
hiddenimports = [
    'streamlit.web.cli',
    'streamlit.runtime.scriptrunner',
    'streamlit.runtime.scriptrunner.magic_funcs',
    'altair',
    'openpyxl',
]

for pkg in ['streamlit', 'plotly', 'pandas', 'statsmodels', 'altair', 'pyarrow']:
    tmp = collect_all(pkg)
    datas    += tmp[0]
    binaries += tmp[1]
    hiddenimports += tmp[2]

datas += collect_data_files('openpyxl')

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'PIL', 'pydeck', 'IPython', 'jupyter'],
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
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name='RoastimeAnalyzer',
)
