from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from database import db
from models.paciente import Paciente
from models.avaliacao import Avaliacao
from models.resposta import Resposta
from score import calcular_resumo

avaliacoes_bp = Blueprint("avaliacoes", __name__)

@avaliacoes_bp.route("/api/avaliacoes", methods=["POST"])
def criar_avaliacao():

    dados= request.get_json(silent=True)

    if not isinstance(dados,dict):
        return jsonify({
            "erro":"Envie um Json valido."
        }), 400

    paciente_id = dados.get("paciente_id")

    if type(paciente_id) is not int or paciente_id <= 0:
        return jsonify({
            "erro": "Informe um paciente_id inteiro positivo."
        }), 400

    paciente = db.session.get(Paciente,paciente_id)

    if paciente is None:
        return jsonify({
            "erro": "Paciente nao encontrado."
        }), 404

    avaliacao =Avaliacao(
        paciente_id=paciente.id
        )

    try:
        db.session.add(avaliacao)
        db.session.commit()

        return jsonify({
            "mensagem":"Avaliacao criada com sucesso.",
            "avaliacao":{
                "id":avaliacao.id,
                "paciente_id":avaliacao.paciente_id,
                "data_avaliacao":avaliacao.data_avaliacao.isoformat(),
                "pontuacao":avaliacao.pontuacao,
                "resultado":avaliacao.resultado
            }
        }), 201
    except SQLAlchemyError:
        db.session.rollback()

        return jsonify({
            "erro":"Nao foi possivel criar a avaliacao."
        }), 500


@avaliacoes_bp.route(
    "/api/avaliacoes/<int:avaliacao_id>/resumo",
    methods=["GET"]
)

def consultar_resumo(avaliacao_id):

    avaliacao = db.session.get(Avaliacao, avaliacao_id)

    if avaliacao is None:
        return jsonify({
            "erro":"Avaliacao nao encontrada."
        }), 404
    respostas = (
        Resposta.query
        .filter_by(avaliacao_id=avaliacao_id)
        .all()
    )

    if not respostas:
        return jsonify({
            "erro":"Esta avaliacao ainda nao possui respostas."
        }), 409

    resumo = calcular_resumo(respostas)

    return jsonify({
        "avaliacao_id":avaliacao_id,
        "paciente_id": avaliacao.paciente_id,
        "resumo":resumo,
        "aviso":"Resumo descritivo , nao representa diagnostivo ou classificacao de risco."
    }), 200
