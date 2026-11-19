import sys
import getpass
import bcrypt

from pathlib import Path

#permite importar os arquivos do backend
PASTA_BACKEND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PASTA_BACKEND))

from app import app
from database import db
from models.usuario import Usuario
from sqlalchemy.exc import SQLAlchemyError


def criar_admin():
    with app.app_context():

        #verifica se ja existe administrador
        admin = Usuario.query.filter_by(
            perfil="administrador"
        ).first()

        if admin is not None:
            print("Ja existe um administrador cadastrado.")
            return

        #solicita os dados no terminal
        nome = input("Nome do administrador: ").strip()
        email = input("Email do administrador: ").strip().lower()
        senha = getpass.getpass("Senha (minimo 12 caracteres): ")

        #valida os dados
        if not nome:
            print("Nome obrigatorio.")
            return

        if not email or "@" not in email:
            print("Email invalido.")
            return

        if len(senha) < 12 or len(senha.encode("utf-8")) > 72:
            print("Senha deve ter no minimo 12 caracteres e no maximo 72 bytes.")
            return

        if Usuario.query.filter_by(email=email).first():
            print("Este email ja esta cadastrado.")
            return

        #gera hash da senha com bcrypt
        senha_hash = bcrypt.hashpw(
            senha.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        novo_admin = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            perfil="administrador"
        )

        try:
            db.session.add(novo_admin)
            db.session.commit()
            print("Administrador criado com sucesso!")

        except SQLAlchemyError:
            db.session.rollback()
            print("Erro ao criar administrador.")


if __name__ == "__main__":
    criar_admin()
