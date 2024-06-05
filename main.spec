# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('env/Lib/site-packages/sc2reader/data/*', 'sc2reader/data'),
        ('env/Lib/site-packages/sc2reader/data/WoL*', 'sc2reader/data/WoL'),
        ('env/Lib/site-packages/sc2reader/data/HotS*', 'sc2reader/data/HotS'),
        ('env/Lib/site-packages/sc2reader/data/LotV*', 'sc2reader/data/LotV'),
    ],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
