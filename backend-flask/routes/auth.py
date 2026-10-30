from flask import Blueprint, jsonify, request,session
from werkzeug.security import check_password_hash
from models.usuario import Usuario
from limiter import limiter
import bcrypt


#verificar senha bcrypt ou werkzeug

def verificar_senha(senha, senha_hash):

    if not isinstance(senha_hash, str):
        return False

    #vefifica se o hash foi criaco com bcrypt
    if senha_hash.startswith(("$2a$","$2b$","$2y$")):
        try:
            return bcrypt.checkpw(
                senha.encode("utf-8"),
                senha_hash.encode("utf-8")
            )
        except(ValueError, OverflowError):
            return False
    #veficiar senhas antigas do werkzeuug

    try:
        return check_password_hash(senha_hash,senha)
    except(ValueError,TypeError):
        return False


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/login", methods=["POST"])
@limiter.limit("5 per minute")
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

    if usuario is None or not verificar_senha(
        senha, usuario.senha_hash
    ):
        return jsonify({
            "erro":"Email ou senha incorretos"
        }), 401

    session.clear()
    session.permanent = True
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

#api para verificar se usuario esta logado
@auth_bp.route("/api/sessao", methods=["GET"])
def consultar_sessao():

    usuario_id = session.get("usuario_id")

    if usuario_id is None:
        return jsonify({
            "erro":"Login necessario."
        }), 401

    usuario = Usuario.query.filter_by(id=usuario_id).first()

    if usuario is None:
        session.clear()
        return jsonify({
            "erro":"Login necessario."
        }), 401

    return jsonify({
        "usuario":{
            "id":usuario.id,
            "nome":usuario.nome,
            "email":usuario.email
        }
    }), 200