__author__ = 'tinyms'

#import sys
from cx_Freeze import setup, Executable
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(
    name="ArchiveX",
    version="1.1",
    description="WaterPress for football match game",
    options={"build_exe": {"includes": ["psycopg2._psycopg","lottery.parse"
        ,"tinyms.core.orm","sqlalchemy.dialects.sqlite","sqlalchemy.dialects.postgresql"]}},
    executables=[Executable(script="ArchiveX.py",
                            targetName="ArchiveX.exe",
                            icon= "static/images/web_card.ico",
                            base=base)])
