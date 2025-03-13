from firebase.config import firebase

def check_book_exists(title, book_id_to_ignore=None) -> bool:
    """Verifica se um livro já existe no Firebase."""
    books = firebase.database().child("books").get()
    if books.each():
        for book in books.each():
            book_data = book.val()
            book_id = book.key()

            # Se for o próprio livro que está sendo editado, ignoramos
            if book_id_to_ignore and book_id == book_id_to_ignore:
                continue

            if book_data["title"].lower() == title.lower():
                return True  # Encontrou um livro com o mesmo título

    return False  # Não encontrou nenhum livro duplicado

def register(book):
    """Registra um novo livro no Firebase."""
    firebase_db = firebase.database()
    instance = firebase_db.child("books").push(book)
    return instance

def update(book_id, updated_book):
    """Atualiza um livro no Firebase."""
    firebase_db = firebase.database()
    instance = firebase_db.child("books").child(book_id).update(updated_book)
    return instance

def delete(book_id):
    """Deleta um livro do Firebase."""
    firebase_db = firebase.database()
    instance = firebase_db.child("books").child(book_id).remove()
    return instance

def get(book_id):
    """Obtém um livro do Firebase."""
    firebase_db = firebase.database()
    book = firebase_db.child("books").child(book_id).get().val()
    return book

def list_():
    """Lista todos os livros do Firebase."""
    firebase_db = firebase.database()
    books = firebase_db.child("books").get()
    return books

