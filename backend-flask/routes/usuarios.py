
from flask import Blueprint, jsonify, request
import bcrypt
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database import db
from models.usuario import Usuario
from auth_utils import admin_required


usuarios_bp = Blueprint("usuarios", __name__)

#cadastro de usuario API
@usuarios_bp.route("/api/usuarios", methods=["POST"])
@admin_required
def cadastrar_usuario():
    dados = request.get_json(silent=True)

    #se n for dicionario rejeita
    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um JSON valido."}), 400

    #capta os dados do json
    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    #valida os dados
    if not isinstance(nome, str) or not nome.strip():
        return jsonify({"erro": "Nome invalido."}), 400

    if not isinstance(email, str) or not email.strip():
        return jsonify({"erro": "Email invalido."}), 400

    #senha precisa ter pelo menos 12 caracteres
    if not isinstance(senha, str) or len(senha) < 12:
        return jsonify({
            "erro": "A senha deve possuir pelo menos 12 caracteres."
        }), 400

    #verifica limite de 72 bytes do bcrypt
    if len(senha.encode("utf-8")) > 72:
        return jsonify({
            "erro": "Senha muito longa."
        }), 400

    #email minusculo
    email = email.strip().lower()

    #validacao email
    if len(nome.strip()) > 120 or len(email) > 150 or "@" not in email:
        return jsonify({"erro": "Nome ou email invalido."}), 400

    #gera o hash da senha com bcrypt
    senha_hash = bcrypt.hashpw(
        senha.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    usuario = Usuario(
        nome=nome.strip(),
        email=email,
        senha_hash=senha_hash
    )

    #tenta adicionar ao banco de dados
    try:
        db.session.add(usuario)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"erro": "Email ja cadastrado."}), 409
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao cadastrar usuario."}), 500

    #cadastra ao banco
    return jsonify({
        "mensagem": "Usuario cadastrado com sucesso.",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        }
    }), 201
