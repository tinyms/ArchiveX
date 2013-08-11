__author__ = 'tinyms'

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="WaterPress",
    version="1.0",
    description="WaterPress for football match game",
    options={"build_exe": {"includes": ["psycopg2._psycopg","lottery.parse"]}},
    executables=[Executable(script="ArchiveX.py",
                            targetName="WaterPress.exe",
                            icon= "static/images/web.ico",
                            base=base)])
