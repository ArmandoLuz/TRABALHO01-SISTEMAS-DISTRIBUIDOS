import firebase_admin
from firebase_admin import credentials
import pyrebase
import os
from dotenv import load_dotenv
import zipfile

# Caminho para o arquivo ZIP e para a pasta onde será extraído
path_zip_config = "./firebase/firebase_config.zip"
destiny = "./firebase"

# Abrir e extrair
with zipfile.ZipFile(path_zip_config, "r") as zip_ref:
    zip_ref.extractall(destiny)

# Obtém o caminho absoluto do diretório do script atual
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, "..", ".env")

# Carrega o .env corretamente
load_dotenv(env_path)

# Configuração do Firebase Admin SDK
cred = credentials.Certificate("firebase/firebase_config.json")
firebase_admin.initialize_app(cred)

# Configuração do Pyrebase para autenticação do usuário
config = {
    "apiKey": os.getenv("API_KEY"),
    "authDomain": os.getenv("AUTHDOMAIN"),
    "databaseURL": os.getenv("DATABASEURL"),
    "storageBucket": os.getenv("STORAGEBUCKET"),
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
