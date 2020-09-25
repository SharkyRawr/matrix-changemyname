import sys
from PyQt5.QtWidgets import QApplication

def compileUI():
    from PyQt5.uic import compileUiDir
    compileUiDir('ui')


if __name__ == "__main__":

    if __debug__:
        compileUI()
    from ui.py_mainwindow import MainWindow

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
