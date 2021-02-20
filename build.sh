#! /bin/sh

# Should probably make a script of this at time point
pyuic5 -o ui/login_dialog.py ui/login_dialog.ui
pyuic5 -o ui/mainwindow.py ui/mainwindow.ui
pyuic5 -o ui/emojieditor.py ui/emojieditor.ui
pyuic5 -o ui/ImportExportHandlerAndProgressDialog.py ui/ImportExportHandlerAndProgressDialog.ui
pyrcc5 -o res/res.py res/res.qrc
PYTHONOPTIMIZE=1 python -OO -m PyInstaller pymain.py -F --add-data ui:ui
