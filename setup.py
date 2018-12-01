from cx_Freeze import setup, Executable
import sys, os

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "program",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]main.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     "icon.ico",                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]

base = None
if sys.platform == "win32": base = "Win32GUI"

msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data}

executables = [Executable("main.pyw", shortcutName='Pong', shortcutDir='DesktopFolder', icon='icon.ico', base=base), Executable("extras.pyw")]

setup(
    name = 'Pong',
    author = 'Ethan Armstrong',
    options={
        "build_exe": {
            "packages":["pygame", "sys", "random", "os"],
            "include_files":["settings.txt", "icon.ico"]
            }},
    executables = executables,
    version = "1.0"
)