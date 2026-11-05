import secrets

from flask import Blueprint, jsonify, request, session

csrf_bp = Blueprint("csrf", __name__)

@csrf_bp.route("/api/csrf-token",methods=["GET"])
def obter_token():

    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)

    return jsonify({
        "csrf_token": session["csrf_token"]
    }), 200

@csrf_bp.before_app_request
def verfificar_csrf():

    #requisicoes de consulta nao precisam de token
    if request.method in ("GET", "HEAD","OPTIONS"):
        return None



    token_esperado = session.get("csrf_token")
    token_recebido = request.headers.get("X-CSRF-Token")

    if(
        not token_esperado
        or not token_recebido
        or not secrets.compare_digest(token_esperado, token_recebido)
    ):
        return jsonify({
            "erro":"Token CSRF ausente ou invalido."
        }), 403

    return None
