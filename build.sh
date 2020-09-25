#! /bin/sh
PYTHONOPTIMIZE=1 python -OO -m PyInstaller pymain.py -F --add-data ui:ui
