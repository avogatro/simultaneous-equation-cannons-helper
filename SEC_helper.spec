# -*- mode: python ; coding: utf-8 -*-
# Please read about Pyinstaller before using this file to create exe for windows
# https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/packaging/pyinstaller/index.html
# https://kivy.org/doc/stable/guide/packaging-windows.html

import sys
import os

from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path

path = os.path.abspath(".")

a = Analysis(
    ['main.py'],
    pathex=[path],
    binaries=[],
    datas=[('assets/images/SEC.png', 'assets/images'),('configurations.ini','.'),('View/EditInputScreen/edit_input_screen.kv','.'),('View/AppMainScreen/app_main_screen.kv','.'), \
		('View/TutorialScreen/tutorial_screen.kv','.'),('assets/icons/icon.png','assets/icons')],
    hiddenimports=[],
    hookspath=[kivymd_hooks_path],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    name='SEC_helper',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='x86_64',
    codesign_identity=None,
    entitlements_file=None,
	icon='icon.ico',
)
