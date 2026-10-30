"""Configurações carregadas das variáveis de ambiente."""
import os
from pathlib import Path
from urllib.parse import quote_plus
from datetime import timedelta
from dotenv import load_dotenv

# Lê o arquivo .env que fica na mesma pasta que app.py.
load_dotenv(Path(__file__).resolve().parent / ".env")


class Config:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "xfragil")
    DB_USER = os.getenv("DB_USER", "xfragil_app")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    SECRET_KEY = os.getenv("SECRET_KEY")

    if not DB_PASSWORD or not SECRET_KEY:
        raise RuntimeError("Configure DB_PASSWORD e SECRET_KEY no arquivo .env")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    # Para produção usando HTTPS, defina COOKIE_SECURE=true no .env.
    SESSION_COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
