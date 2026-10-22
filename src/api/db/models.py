from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, validates

from db.database import Base
from db.senhas import gerar_hash


class User(Base):
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    senha: Mapped[str] = mapped_column(String)

    @validates('senha')
    def salvar_senha(self, campo, senha):
        return gerar_hash(senha)
