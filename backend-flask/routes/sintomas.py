from flask import Blueprint, jsonify, request
from models.sintoma import Sintoma

sintomas_bp = Blueprint("sintomas", __name__)

@sintomas_bp.route("/api/sintomas", methods=["GET"])
def listar_sintomas():
    sexo = request.args.get("sexo", "").strip().lower()

    if sexo not in ("masculino","feminino"):
        return jsonify({
            "erro": "Informe sexo = masculino ou sexo = feminino"
        }), 400

    sintomas = (
        Sintoma.query
        .filter(
            Sintoma.ativo.is_(True),
            Sintoma.sexo_aplicavel.in_(["ambos", sexo])
        )
        .order_by(Sintoma.id)
        .all()
    )

    resultado = [
        {
            "id": sintoma.id,
            "descricao":sintoma.descricao
        }
        for sintoma in sintomas
    ]

    return jsonify({
        "sexo":sexo,
        "total":len(resultado),
        "sintomas":resultado
    }), 200
