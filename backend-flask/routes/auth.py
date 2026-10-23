from flask import Blueprint, jsonify, request,session
from werkzeug.security import check_password_hash
from models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/login", methods=["POST"])
def login():
    dados = request.get_json(silent=True)

    if not isinstance(dados,dict):
        return jsonify({
            "erro":"Envie um JSON valido."
        }), 400

    email = dados.get("email")
    senha = dados.get("senha")

    if not isinstance(email,str) or not isinstance(senha,str):
        return jsonify({
            "erro":"Email e senha sao obrigatorios."
        }), 400

    email = email.strip().lower()

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario is None or not check_password_hash(
        usuario.senha_hash, senha
    ):
        return jsonify({
            "erro":"Email ou senha incorretos"
        }), 401

    session.clear()
    session["usuario_id"]=usuario.id

    return jsonify({
        "mensagem":"Credenciais verificadas com sucesso.",
        "usuario":{
            "id":usuario.id,
            "nome":usuario.nome,
            "email":usuario.email
        }
    }), 200


@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({
        "mensagem": "Logout realizado com sucesso."
    }), 200
