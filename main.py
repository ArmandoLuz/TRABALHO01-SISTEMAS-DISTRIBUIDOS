from PyQt6.QtWidgets import QApplication
from gui.auth.auth_window import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
