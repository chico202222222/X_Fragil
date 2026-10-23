
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from database import db
from models.avaliacao import Avaliacao
from models.paciente import Paciente
from models.sintoma import Sintoma
from models.resposta import Resposta


respostas_bp = Blueprint("respostas", __name__)


@respostas_bp.route(
    "/api/avaliacoes/<int:avaliacao_id>/respostas",
    methods=["POST"]
)
def registrar_respostas(avaliacao_id):
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um JSON valido."}), 400

    respostas = dados.get("respostas")

    if not isinstance(respostas, list):
        return jsonify({"erro": "Informe uma lista de respostas."}), 400

    avaliacao = db.session.get(Avaliacao, avaliacao_id)

    if avaliacao is None:
        return jsonify({"erro": "Avaliacao nao encontrada."}), 404

    paciente = db.session.get(Paciente, avaliacao.paciente_id)

    if paciente is None:
        return jsonify({"erro": "Paciente nao encontrado."}), 404

    sintomas = Sintoma.query.filter(
        Sintoma.ativo.is_(True),
        Sintoma.sexo_aplicavel.in_(["ambos", paciente.sexo])
    ).all()

    ids_permitidos = {s.id for s in sintomas}
    ids_recebidos = set()

    if len(respostas) != len(ids_permitidos):
        return jsonify({
            "erro": "Envie uma resposta para cada sintoma do checklist."
        }), 400

    for resposta in respostas:
        if not isinstance(resposta, dict):
            return jsonify({"erro": "Resposta invalida."}), 400

        sintoma_id = resposta.get("sintoma_id")
        presente = resposta.get("presente")

        if type(sintoma_id) is not int:
            return jsonify({"erro": "sintoma_id invalido."}), 400

        if type(presente) is not bool:
            return jsonify({"erro": "presente deve ser true ou false."}), 400

        if sintoma_id not in ids_permitidos:
            return jsonify({
                "erro": "Sintoma nao pertence ao checklist."
            }), 400

        if sintoma_id in ids_recebidos:
            return jsonify({
                "erro": "Sintoma duplicado na requisicao."
            }), 400

        ids_recebidos.add(sintoma_id)

    existente = Resposta.query.filter_by(
        avaliacao_id=avaliacao_id
    ).first()

    if existente is not None:
        return jsonify({
            "erro": "Esta avaliacao ja possui respostas."
        }), 409

    try:
        for resposta in respostas:
            nova_resposta = Resposta(
                avaliacao_id=avaliacao_id,
                sintoma_id=resposta["sintoma_id"],
                presente=resposta["presente"]
            )
            db.session.add(nova_resposta)

        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "erro": "Nao foi possivel salvar as respostas."
        }), 500

    return jsonify({
        "mensagem": "Respostas registradas com sucesso.",
        "avaliacao_id": avaliacao_id,
        "total_respostas": len(respostas)
    }), 201


@respostas_bp.route(
    "/api/avaliacoes/<int:avaliacao_id>/respostas",
    methods=["GET"]

)
def listar_respostas(avaliacao_id):

    avaliacao = db.session.get(Avaliacao, avaliacao_id)

    if avaliacao is None:
        return jsonify({
            "erro":"Avaliacao nao encontrada."
        }), 404

    respostas = (
        Resposta.query
        .filter_by(avaliacao_id=avaliacao_id)
        .order_by(Resposta.sintoma_id)
        .all()
    )

    resultado = [
        {
            "sintoma_id" : resposta.sintoma_id,
            "descricao": resposta.sintoma.descricao,
            "presente":resposta.presente
        }
        for resposta in respostas
    ]

    return jsonify({
        "avaliacao_id":avaliacao_id,
        "total":len(resultado),
        "respostas":resultado
    }), 200