import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
HF_TOKEN = os.getenv("HF_TOKEN")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada en el archivo .env")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN no está configurado en el archivo .env")