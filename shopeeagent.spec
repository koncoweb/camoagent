import sys
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files, collect_all

block_cipher = None

# Collect all necessary data and imports
hiddenimports_list = [
    'crewai',
    'crewai_tools',
    'camoufox',
    'camoufox.sync_api',
    'crewai.agents',
    'crewai.tasks',
    'crewai.crews',
    'crewai.llms',
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'PyQt6.sip',
    'pydantic',
    'pydantic_settings',
    'dotenv',
    'markdown',
    'markdown.extensions',
    'browserforge',
    'browserforge.fingerprints',
    'browserforge.fingerprints.Screen',
    'browserforge.fingerprints.FingerprintGenerator',
    'yaml',
    'yaml.cyaml',
]

# Add all crewai submodules
hiddenimports_list += collect_submodules('crewai')
hiddenimports_list += collect_submodules('crewai_tools')

# Collect data files
datas_list = [
    ('config', 'config'),
]

# Add PyQt6 plugins data
try:
    from PyInstaller.utils.hooks import qt_plugins
    for plugin_type, plugin_name in qt_plugins.get_qt6_plugins().items():
        datas_list.append((f'PyQt6/{plugin_name}', f'PyQt6/{plugin_name}'))
except:
    pass

# Collect crewai data
for mod in ['crewai', 'crewai_tools']:
    try:
        data = collect_data_files(mod)
        datas_list.extend(data)
    except:
        pass

a = Analysis(
    ['camoagent.py'],
    pathex=[os.getcwd(), os.path.dirname(sys.executable)],
    binaries=[],
    datas=datas_list,
    hiddenimports=hiddenimports_list,
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
    name='ShopeeAgent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version=None,
    manifest=None,
    console=False,
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
