from firebase_admin import auth
from firebase.config import auth as client_auth  # Importa o auth do Pyrebase

def user_register(email, password):
    """Registra um novo usuário no Firebase."""
    user = auth.create_user(email=email, password=password)
    return user

def user_login(email, password):
    """Autentica o usuário no Firebase."""
    user = client_auth.sign_in_with_email_and_password(email, password)
    return user
