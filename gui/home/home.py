from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt


class DashboardWindow(QWidget):
    def __init__(self, on_logout):
        super().__init__()

        self.setWindowTitle("Painel do Usuário")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        self.label_welcome = QLabel("🎉 Bem-vindo ao sistema de biblioteca!")
        self.label_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_welcome.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")

        self.btn_logout = QPushButton("Sair")
        self.btn_logout.setStyleSheet("background-color: red; color: white; font-size: 14px; padding: 5px;")
        self.btn_logout.clicked.connect(on_logout)

        layout.addWidget(self.label_welcome)
        layout.addWidget(self.btn_logout)

        self.setLayout(layout)
