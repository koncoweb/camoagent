import sys
import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

a = Analysis(
    ['camoagent.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('.env', '.'),
    ],
    hiddenimports=[
        'crewai',
        'crewai_tools',
        'camoufox',
        'camoufox.sync_api',
        'camoufox.options',
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'pydantic',
        'python_dotenv',
        'dotenv',
        'asyncio',
        'aiofiles',
        'websocket',
        'websocket_client',
        'PIL',
        'PIL.Image',
        'io',
        'io.BytesIO',
    ] + collect_submodules('crewai') + collect_submodules('crewai_tools'),
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CamoAgent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='CamoAgent',
)
