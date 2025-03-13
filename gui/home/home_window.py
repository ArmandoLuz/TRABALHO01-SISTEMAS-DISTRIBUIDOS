from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QMessageBox
)

from core.book.usecases import register_book, update_book, delete_book, list_books
from firebase.config import firebase


class HomeWindow(QWidget):
    def __init__(self, logout_callback):
        super().__init__()
        self.firebase_db = firebase.database()
        self.logout_callback = logout_callback
        self.current_book_id = None  # Para rastrear o livro em edição

        self.setWindowTitle("Home - Biblioteca")
        self.showMaximized()
        self.layout = QVBoxLayout()

        # Campos de entrada
        self.input_title = QLineEdit()
        self.input_author = QLineEdit()
        self.input_pages = QLineEdit()
        self.input_year = QLineEdit()

        # Botões
        self.btn_add = QPushButton("Adicionar Livro")
        self.btn_add.clicked.connect(self.add_book)

        self.btn_update = QPushButton("Atualizar Livro")
        self.btn_update.clicked.connect(self.update_book)
        self.btn_update.setEnabled(False)

        self.btn_delete = QPushButton("Excluir Livro")
        self.btn_delete.clicked.connect(self.delete_book)
        self.btn_delete.setEnabled(False)

        self.btn_logout = QPushButton("Sair")
        self.btn_logout.clicked.connect(self.logout)
        self.btn_logout.setStyleSheet(
            "background-color: red; color: white; font-weight: bold; padding: 5px; border-radius: 5px;"
        )

        # Tabela de livros
        self.book_table = QTableWidget()
        self.book_table.setColumnCount(4)
        self.book_table.setHorizontalHeaderLabels(["Título", "Autor", "Páginas", "Ano"])
        self.book_table.cellClicked.connect(self.load_book_to_edit)

        # Adiciona os widgets ao layout
        self.layout.addWidget(QLabel("Título"))
        self.layout.addWidget(self.input_title)
        self.layout.addWidget(QLabel("Autor"))
        self.layout.addWidget(self.input_author)
        self.layout.addWidget(QLabel("Páginas"))
        self.layout.addWidget(self.input_pages)
        self.layout.addWidget(QLabel("Ano"))
        self.layout.addWidget(self.input_year)

        self.layout.addWidget(self.btn_add)
        self.layout.addWidget(self.btn_update)
        self.layout.addWidget(self.btn_delete)
        self.layout.addWidget(self.book_table)
        self.layout.addWidget(self.btn_logout)

        self.setLayout(self.layout)
        self.load_books()

    def add_book(self):
        title = self.input_title.text().strip()
        author = self.input_author.text().strip()
        pages = self.input_pages.text().strip()
        year = self.input_year.text().strip()

        if not title or not author or not pages or not year:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return

        message, status = register_book(title, author, pages, year)

        if not status:
            QMessageBox.warning(self, "Erro", message)
            return
        else:
            self.load_books()
            QMessageBox.information(self, "Sucesso", message)

    def update_book(self):
        if self.current_book_id:
            updated_book = {
                "title": self.input_title.text(),
                "author": self.input_author.text(),
                "pages": self.input_pages.text(),
                "year": self.input_year.text()
            }

            message, status = update_book(self.current_book_id, updated_book)

            if not status:
                QMessageBox.warning(self, "Erro", message)
                return
            else:
                QMessageBox.information(self, "Sucesso", message)
                self.load_books()
                self.clear_fields()

    def delete_book(self):
        if self.current_book_id:
            response = QMessageBox.question(
                self,
                "Excluir Livro",
                "Tem certeza que deseja excluir este livro?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if response == QMessageBox.StandardButton.Yes:
                message, _ = delete_book(self.current_book_id)
                QMessageBox.information(self, "Sucesso", message)
                self.load_books()
                self.clear_fields()

    def load_books(self):
        self.book_table.setRowCount(0)
        books = list_books()
        if books.each():
            for i, book in enumerate(books.each()):
                data = book.val()
                self.book_table.insertRow(i)
                self.book_table.setItem(i, 0, QTableWidgetItem(data["title"]))
                self.book_table.setItem(i, 1, QTableWidgetItem(data["author"]))
                self.book_table.setItem(i, 2, QTableWidgetItem(str(data["pages"])))
                self.book_table.setItem(i, 3, QTableWidgetItem(str(data["year"])))

    def load_book_to_edit(self, row):
        self.current_book_id = list(list_books().val().keys())[row]
        book = self.firebase_db.child("books").child(self.current_book_id).get().val()
        self.input_title.setText(book["title"])
        self.input_author.setText(book["author"])
        self.input_pages.setText(str(book["pages"]))
        self.input_year.setText(str(book["year"]))
        self.btn_update.setEnabled(True)
        self.btn_delete.setEnabled(True)

    def clear_fields(self):
        self.input_title.clear()
        self.input_author.clear()
        self.input_pages.clear()
        self.input_year.clear()
        self.current_book_id = None
        self.btn_update.setEnabled(False)
        self.btn_delete.setEnabled(False)

    def logout(self):
        self.logout_callback()