from core.book.repositories import check_book_exists, register, update, delete, list_, get


def register_book(title, author, pages, year):
    exists = check_book_exists(title)
    if exists:
        return "❌ O livro já está cadastrado", False

    new_book = {
        "title": title,
        "author": author,
        "pages": pages,
        "year": year
    }

    instance = register(new_book)
    if instance:
        return "✅ Livro cadastrado com sucesso", True
    return "❌ Erro ao cadastrar livro", False

def update_book(book_id, updated_book):
    title_already_exists = check_book_exists(updated_book["title"], book_id_to_ignore=book_id)
    if title_already_exists:
        return "❌ Já existe um livro com esse título", False

    instance = update(book_id, updated_book)

    if instance:
        return "✅ Livro atualizado com sucesso", True
    return "❌ Erro ao atualizar livro", False

def delete_book(book_id):
    delete(book_id)
    return "✅ Livro excluído com sucesso", True

def get_book(book_id):
    try:
        book = get(book_id)
        return book
    except:
        return None

def list_books():
    books = list_()
    return books