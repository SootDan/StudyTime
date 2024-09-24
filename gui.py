"""
TODO: Add module docstring
"""
from sys import argv
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.uic import loadUi


class MainUI(QMainWindow):
    """
    TODO: Add description
    """
    def __init__(self):
        super().__init__()
        loadUi("ui.ui", self)

        self.pushButton.clicked.connect(self.helloworld)


    def helloworld(self):
        """
        Test method
        """
        print("hello, world")


if __name__ == "__main__":
    app = QApplication(argv)
    ui = MainUI()
    ui.show()
    app.exec()
