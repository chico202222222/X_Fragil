from auth_utils import login_required
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from database import db
from models.paciente import Paciente
from models.avaliacao import Avaliacao
from models.resposta import Resposta
from score import calcular_resumo
from flask import session

avaliacoes_bp = Blueprint("avaliacoes", __name__)

@avaliacoes_bp.route("/api/avaliacoes", methods=["POST"])
@login_required
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

    paciente = Paciente.query.filter_by(
        id=paciente_id,
        usuario_id=session["usuario_id"]).first()


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

@login_required
def consultar_resumo(avaliacao_id):

    avaliacao = (
        Avaliacao.query
        .join(Paciente, Avaliacao.paciente_id == Paciente.id)
        .filter(
            Avaliacao.id == avaliacao_id,
            Paciente.usuario_id == session["usuario_id"]
        )
        .first()
    )

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

@avaliacoes_bp.route("/api/pacientes/<int:paciente_id>/avaliacoes",methods=["GET"])
@login_required
def historico_avaliacoes(paciente_id):

    #vefifica se paciente pertence ao profissional
    paciente = Paciente.query.filter_by(
        id=paciente_id,
        usuario_id=session["usuario_id"]
    ).first()

    if paciente is None:
        return jsonify({
            "erro":"Paciente nao encontrado."
        }), 404

    #busca as avaliacoes recentes primeiro
    avaliacoes = (
        Avaliacao.query
        .filter_by(paciente_id=paciente_id)
        .order_by(Avaliacao.data_avaliacao.desc(), Avaliacao.id.desc())
        .all()
    )

    historico = []

    for avaliacao in avaliacoes:
        historico.append({
            "id":avaliacao.id,
            "paciente_id":avaliacao.paciente_id,
            "data_avaliacao": (
                avaliacao.data_avaliacao.isoformat()
                if avaliacao.data_avaliacao else None
            ),
            "pontuacao": avaliacao.pontuacao,
            "resultado": avaliacao.resultado,
            "status": (
                "concluida"
                if avaliacao.pontuacao is not None
                else "pendente"
            )
        })

    return jsonify({
        "paciente_id": paciente_id,
        "total": len(historico),
        "avaliacoes": historico
    }), 200