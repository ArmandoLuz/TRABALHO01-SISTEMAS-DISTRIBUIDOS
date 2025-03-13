from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
)

from core.user.usecases import register, login
from gui.home.home_window import HomeWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.home = None
        self.setWindowTitle("Sistema de Biblioteca")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.label_email = QLabel("Email:")
        self.input_email = QLineEdit()

        self.label_password = QLabel("Senha:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_registrar = QPushButton("Registrar")
        self.btn_registrar.clicked.connect(self.register)

        self.btn_login = QPushButton("Login")
        self.btn_login.clicked.connect(self.login)

        # Label para exibir mensagens (erros e sucesso)
        self.message_label = QLabel("")
        self.message_label.setWordWrap(True)  # Permite quebra de linha

        self.layout.addWidget(self.label_email)
        self.layout.addWidget(self.input_email)
        self.layout.addWidget(self.label_password)
        self.layout.addWidget(self.input_password)
        self.layout.addWidget(self.btn_registrar)
        self.layout.addWidget(self.btn_login)
        self.layout.addWidget(self.message_label)

        self.setLayout(self.layout)

    def show_message(self, text, color):
        """ Exibe uma mensagem estilizada na tela. """
        self.message_label.setText(text)
        self.message_label.setStyleSheet(f"background-color: {color}; color: white; padding: 5px; border-radius: 5px;")

    def register(self):
        message, status = register(
            email=self.input_email.text(),
            password=self.input_password.text()
        )
        color = "green" if status else "red"
        self.show_message(f"{message}", color)

    def login(self):
        message, status = login(
            email=self.input_email.text(),
            password=self.input_password.text()
        )
        if status:
            self.open_home()
        else:
            self.show_message(f"{message}", "red")

    def open_home(self):
        """ Abre o dashboard e esconde a tela de login """
        self.home = HomeWindow(self.logout)
        self.home.show()
        self.hide()  # Esconde a tela de login

    def logout(self):
        """ Fecha o dashboard e retorna à tela de login """
        self.home.close()
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


