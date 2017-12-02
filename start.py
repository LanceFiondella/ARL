import sys
from PyQt5.QtWidgets import QApplication
from gui import windows

if __name__== '__main__':
    app = QApplication(sys.argv)
    window = windows.MainWindow()
    sys.exit(app.exec_())

