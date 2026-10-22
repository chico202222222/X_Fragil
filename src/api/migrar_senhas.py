from sqlalchemy import select

from db.database import database
from db.models import User


def migrar_senhas():
    sessao = database.abrir_sessao()
    quantidade = 0

    try:
        usuarios = sessao.execute(select(User)).scalars().all()
        for usuario in usuarios:
            if not usuario.senha.startswith(('$2a$', '$2b$', '$2y$')):
                # A atribuição passa pelo modelo, que gera o hash.
                usuario.senha = usuario.senha
                quantidade += 1
        sessao.commit()
    except Exception:
        sessao.rollback()
        raise
    finally:
        sessao.close()

    print(f'{quantidade} senha(s) migrada(s) para bcrypt')


if __name__ == '__main__':
    migrar_senhas()
