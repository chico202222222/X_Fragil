import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self):
        url = os.environ.get('DATABASE_URL')
        if url is None:
            db_file = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', '..', '..', 'prisma', 'dev.db'),
            )
            url = f'sqlite:///{db_file}'

        self.engine = create_engine(url)
        self.session_local = sessionmaker(bind=self.engine)

    def abrir_sessao(self):
        return self.session_local()


database = Database()
