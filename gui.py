"""
GUI version of the app.
"""
from sys import argv
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.uic import loadUi
from script import App


class MainUI(QMainWindow, App):
    """
    TODO: Add description
    """
    def __init__(self):
        super().__init__()
        loadUi("ui.ui", self)


if __name__ == "__main__":
    app = QApplication(argv)
    ui = MainUI()
    ui.show()
    app.exec()
