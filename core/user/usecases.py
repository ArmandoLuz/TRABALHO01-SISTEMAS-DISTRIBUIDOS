from firebase_admin.auth import EmailAlreadyExistsError
from requests import HTTPError

from core.user.repositories import user_register, user_login

def register(email: str, password: str) -> tuple[str, bool] | None:
    """Registra um novo usuário no Firebase."""
    try:
        user = user_register(email, password)
        if user:
            return "✅ Usuário registrado com sucesso!", True
    except EmailAlreadyExistsError:
        return f"❌ O email informado já está cadastrado", False
    except ValueError as e:
        return ("❌ Email inválido" if "email" in str(e) \
            else "❌ Senha inválida", False)
    except Exception:
        return "❌ Erro de conexão com o servidor", False

def login(email: str, password: str) -> tuple[str, bool] | None:
    try:
        user = user_login(email, password)
        if user:
            return "✅ Login realizado com sucesso! Redirecionando...", True
    except HTTPError as e:
        return (f"❌ Dados de login inválidos" \
            if "INVALID_LOGIN_CREDENTIALS" in e.strerror or "INVALID_EMAIL" in e.strerror or "INVALID_PASSWORD" in e.strerror \
            else f"❌ Erro inesperado - {e.strerror}", False)