# guia sqlalchemy 15/10/2026

nao vamos mais usar sqlite direto. usamos sqlalchemy pra conectar no banco.

## conectar

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine('mysql+pymysql://user:senha@localhost:3306/banco')
# sqlite de teste: create_engine('sqlite:///dev.db')

Session = sessionmaker(bind=engine)
sessao = Session()
```

no projeto isso fica em database.py. url vem de DATABASE_URL.

## criar tabela (modelo)

```python
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'User'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    senha: Mapped[str] = mapped_column(String)

Base.metadata.create_all(engine)
```

## buscar

```python
from sqlalchemy import select

consulta = select(User).where(User.email == email)
usuario = sessao.execute(consulta).scalar_one_or_none()
# lista: sessao.execute(consulta).scalars().all()
# por id: sessao.get(User, 1)
```

## criar / editar / apagar

```python
novo = User(nome='Maria', email='m@x.com', senha='12345678')
sessao.add(novo)
sessao.commit()

usuario.nome = 'Novo nome'
sessao.commit()

sessao.delete(usuario)
sessao.commit()
sessao.close()
```

sempre fecha a sessao. sem commit a mudanca nao grava.
