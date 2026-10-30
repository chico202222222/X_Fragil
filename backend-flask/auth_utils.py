"""Decorador que bloqueia o acesso de usuários não autenticados."""
from functools import wraps
from flask import jsonify, session
from database import db
from models.usuario import Usuario


def login_required(funcao):
    @wraps(funcao)
    def verificar_login(*args, **kwargs):
        usuario_id = session.get("usuario_id")
        if type(usuario_id) is not int:
            return jsonify({"erro": "Login necessario."}), 401

        if db.session.get(Usuario, usuario_id) is None:
            session.clear()
            return jsonify({"erro": "Sessao invalida."}), 401

        return funcao(*args, **kwargs)

    return verificar_login

def admin_required(funcao):
    @wraps(funcao)
    def verificar_admin(*args, **kwargs):

        usuario_id = session.get("usuario_id")

        if type(usuario_id) is not int:
            return jsonify({"erro":"Login necessario."}), 401


        usuario = db.session.get(Usuario, usuario_id)

        if usuario is None:
            session.clear()
            return jsonify({"erro":"Sessao invalida."}), 401

        if usuario.perfil != "administrador":
            return jsonify({"erro":"Acesso negado."}), 403

        return funcao(*args, **kwargs)

    return verificar_admin
