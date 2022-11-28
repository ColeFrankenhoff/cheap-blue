import sys

from PyQt5.QtWidgets import QApplication

import window
#Window.py handles some imports in addition
#To being a library

def main():
    app = QApplication(sys.argv)
    mainwindow = window.MainWindow()
    mainwindow.show()
    app.exec_()

main()
