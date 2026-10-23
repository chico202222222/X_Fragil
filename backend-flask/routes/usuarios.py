
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database import db
from models.usuario import Usuario


usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/api/usuarios", methods=["POST"])
def cadastrar_usuario():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um JSON valido."}), 400

    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not isinstance(nome, str) or not nome.strip():
        return jsonify({"erro": "Nome invalido."}), 400

    if not isinstance(email, str) or not email.strip():
        return jsonify({"erro": "Email invalido."}), 400

    if not isinstance(senha, str) or len(senha) < 12:
        return jsonify({
            "erro": "A senha deve possuir pelo menos 12 caracteres."
        }), 400

    email = email.strip().lower()

    if len(nome.strip()) > 120 or len(email) > 150 or "@" not in email:
        return jsonify({"erro": "Nome ou email invalido."}), 400

    usuario = Usuario(
        nome=nome.strip(),
        email=email,
        senha_hash=generate_password_hash(senha)
    )

    try:
        db.session.add(usuario)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"erro": "Email ja cadastrado."}), 409
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao cadastrar usuario."}), 500

    return jsonify({
        "mensagem": "Usuario cadastrado com sucesso.",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        }
    }), 201
