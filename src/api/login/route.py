from flask import jsonify, request
from sqlalchemy import select

from db.database import database
from db.models import User


def login():
    print('[login] alguem chamou POST /api/login')

    dados = request.get_json(silent=True)
    if dados is None:
        dados = {}

    print('[login] json recebido:', dados)

    email = dados.get('email', '')
    senha = dados.get('senha', '')

    sessao = database.abrir_sessao()
    try:
        consulta = select(User).where(
            User.email == email,
            User.senha == senha,
        )
        usuario = sessao.execute(consulta).scalar_one_or_none()
    finally:
        sessao.close()

    if usuario is None:
        print('[login] usuario nao encontrado')
        return jsonify({'error': 'Usuário ou senha inválidos'}), 401

    print('[login] ok, id:', usuario.id)
    return jsonify({
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
    })


def registrar_rotas_login(app):
    app.add_url_rule('/api/login', view_func=login, methods=['POST'])
    print('[login] rota POST /api/login registrada')
