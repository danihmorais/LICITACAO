# -*- mode: python ; coding: utf-8 -*-

from datetime import datetime

BUILD_DATE = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

with open("build_info.py", "w", encoding="utf-8") as f:
    f.write(f'BUILD_DATE = "{BUILD_DATE}"\n')
    
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets/'), ('modelos', 'modelos/'), ('settings.json', '.')],
    hiddenimports=[],
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
    a.binaries,
    a.datas,
    [],
    name='Licita.AI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\logo.ico'],
)