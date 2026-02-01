# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for NexDex Windows exe
Build with: pyinstaller nexdex_windows.spec
"""

import sys
from pathlib import Path

block_cipher = None
app_root = Path('.')

a = Analysis(
    ['launcher.py'],
    pathex=[str(app_root)],
    binaries=[],
    datas=[
        ('dashboard/templates', 'dashboard/templates'),
        ('dashboard/static', 'dashboard/static'),
        ('config', 'config'),
        ('scenarios', 'scenarios'),
        ('src', 'src'),
    ],
    hiddenimports=[
        'flask',
        'networkx',
        'matplotlib',
        'jinja2',
        'colorama',
        'tabulate',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NexDex',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window on startup
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/nexdex_icon.ico',
)
