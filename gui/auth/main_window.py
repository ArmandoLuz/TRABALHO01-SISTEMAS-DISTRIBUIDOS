from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
)
from firebase_admin.auth import EmailAlreadyExistsError
from requests import HTTPError

from core.user.auth import user_register, user_login
from gui.home.home import DashboardWindow


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
        email = self.input_email.text()
        password = self.input_password.text()
        try:
            user = user_register(email, password)
            if user:
                self.show_message("✅ Usuário registrado com sucesso!", "green")
        except EmailAlreadyExistsError as exc:
            self.show_message(f"❌ O email informado já está cadastrado", "red")
        except ValueError as e:
            message = "❌ Email inválido" if "email" in str(e) \
                      else "❌ Senha inválida"
            self.show_message(f"❌ Erro no cadastro: {message}", "red")

    def login(self):
        email = self.input_email.text()
        password = self.input_password.text()
        try:
            user = user_login(email, password)
            if user:
                self.show_message("✅ Login realizado com sucesso! Redirecionando...", "green")
                self.open_home()
        except HTTPError as e:
            print(type(e.strerror))
            message = f"❌ dados de login inválidos" \
                      if "INVALID_LOGIN_CREDENTIALS" in e.strerror or "INVALID_EMAIL" in e.strerror or "INVALID_PASSWORD" in e.strerror \
                      else f"❌ Erro inesperado - {e.strerror}"

            self.show_message(f"❌ Erro no login: {message}", "red")

    def open_home(self):
        """ Abre o dashboard e esconde a tela de login """
        self.home = DashboardWindow(self.logout)
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


