import unittest
from unittest.mock import patch

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker

from db.database import Base, database
from db.models import User
from db.senhas import gerar_hash, verificar_senha
from migrar_senhas import migrar_senhas
with patch.dict('os.environ', {'SECRET_KEY': 'chave-apenas-para-testes', 'APP_ENV': 'test'}):
    from server import app


class TestSenhas(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://')
        Base.metadata.create_all(self.engine)
        self.sessoes = sessionmaker(bind=self.engine)
        self.patch = patch.object(database, 'session_local', self.sessoes)
        self.patch.start()
        self.client = app.test_client()

    def tearDown(self):
        self.patch.stop()
        self.engine.dispose()

    def test_hash(self):
        hash_salvo = gerar_hash('senha123')
        self.assertNotEqual(hash_salvo, 'senha123')
        self.assertTrue(verificar_senha('senha123', hash_salvo))
        self.assertFalse(verificar_senha('errada', hash_salvo))
        self.assertFalse(verificar_senha('senha123', 'texto puro'))
        self.assertFalse(verificar_senha('a' * 73, hash_salvo))
        with self.assertRaises(ValueError):
            gerar_hash('á' * 37)

    def test_login(self):
        with self.sessoes() as sessao:
            usuario = User(nome='Teste', email='teste@email.com', senha='senha123')
            self.assertTrue(usuario.senha.startswith('$2b$'))
            sessao.add(usuario)
            sessao.commit()

        resposta = self.client.post('/api/login', json={
            'email': 'teste@email.com', 'senha': 'senha123',
        })
        self.assertEqual(resposta.status_code, 200)
        self.assertNotIn('senha', resposta.get_json() or {})
        self.assertEqual(self.client.get('/api/sessao').status_code, 200)
        self.client.post('/api/logout')
        self.assertEqual(self.client.get('/api/sessao').status_code, 401)

        for email, senha in [('teste@email.com', 'errada'), ('outro@email.com', 'senha123')]:
            resposta = self.client.post('/api/login', json={'email': email, 'senha': senha})
            self.assertEqual(resposta.status_code, 401)

        for dados in [[], {'senha': 123}, {'senha': 'a' * 73}]:
            self.assertEqual(self.client.post('/api/login', json=dados).status_code, 400)

    def test_migracao(self):
        with self.engine.begin() as conexao:
            conexao.execute(text(
                'INSERT INTO "User" (nome, email, senha) VALUES (:nome, :email, :senha)'
            ), {'nome': 'Teste', 'email': 'teste@email.com', 'senha': 'senha123'})

        migrar_senhas()
        with self.sessoes() as sessao:
            hash_salvo = sessao.execute(select(User.senha)).scalar_one()
            self.assertTrue(verificar_senha('senha123', hash_salvo))

        migrar_senhas()
        with self.sessoes() as sessao:
            self.assertEqual(sessao.execute(select(User.senha)).scalar_one(), hash_salvo)


if __name__ == '__main__':
    unittest.main()
