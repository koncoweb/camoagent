# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

site_pkg = r"C:\Users\THINKPAD\AppData\Local\Programs\Python\Python311\Lib\site-packages"

a = Analysis(
    ['camoagent.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        (os.path.join(site_pkg, 'crewai', 'translations'), 'crewai/translations'),
        (os.path.join(site_pkg, 'apify_fingerprint_datapoints', 'data'), 'apify_fingerprint_datapoints/data'),
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
        'pydantic_settings',
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
        'markdown',
        'browserforge',
        'browserforge.fingerprints',
        'browserforge.headers',
        'browserforge.headers.generator',
        'browserforge.bayesian_network',
        'apify_fingerprint_datapoints',
        'yaml',
    ],
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
    icon='logoicon-removebg-preview.ico',
    name='ShopeeAgent',
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
    name='ShopeeAgent',
)
