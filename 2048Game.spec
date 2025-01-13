# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['ui.py'],
    pathex=[r'k:/0_learning a new skill/games/game_2048/vsimp_2048'],
    binaries=[],
    datas=[('saves', 'saves')],
    hiddenimports=['ttkbootstrap', 'grid'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='2048Game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False if you want to hide the console window
    icon='icon.ico'  # Add an icon file if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='2048Game'
)