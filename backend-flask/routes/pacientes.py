from datetime import date
from auth_utils import login_required
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from database import db
from models.paciente import Paciente

pacientes_bp = Blueprint("pacientes",__name__)


@pacientes_bp.route("/api/pacientes", methods=["POST"])
@login_required
def cadastrar_paciente():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro":"Envie um JSON valido."
        }), 400

    nome = dados.get("nome")
    nascimento = dados.get("data_nascimento")
    sexo = dados.get("sexo")

    if not isinstance(nome, str) or not nome.strip():
        return jsonify({
            "erro":"Nome e obrigatorio."
        }), 400

    if not isinstance(nascimento, str):
        return jsonify({
            "erro": "Data de nascimento e obrigatoria."
        }), 400

    try:
        data_nascimento = date.fromisoformat(nascimento)
    except ValueError:
        return jsonify({
            "erro": "Use data_nascimento no formato AAAA-MM-DD."
        }), 400

    if data_nascimento> date.today():
        return jsonify({
            "erro": "Data de nascimento nao pode ser futura."
        }), 400

    if not isinstance(sexo, str):
        return jsonify({
            "erro":"Sexo deve ser masculino ou feminino."
        }), 400

    sexo = sexo.strip().lower()

    if sexo not in ("masculino", "feminino"):
        return jsonify({
            "erro":"Sexo deve ser masculino ou feminino."
        }), 400

    paciente = Paciente(
        nome=nome.strip(),
        data_nascimento=data_nascimento,sexo=sexo
    )

    try:
        db.session.add(paciente)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "erro": "Nao foi possivel cadastrar o paciente"
        }), 500

    return jsonify({
        "mensagem":"Paciente cadastrado com sucesso.",
        "paciente":{
            "id":paciente.id,
            "nome":paciente.nome,
            "data_nascimento": paciente.data_nascimento.isoformat(),
            "sexo": paciente.sexo
        }
    }) , 201

@pacientes_bp.route("/api/pacientes", methods=["GET"])
@login_required
def listar_pacientes():
    pacientes = Paciente.query.order_by(Paciente.id).all()

    resultado = [
        {
            "id":paciente.id,
            "nome":paciente.nome,
            "data_nascimento": paciente.data_nascimento.isoformat(),
            "sexo": paciente.sexo
        }
        for paciente in pacientes
    ]

    return jsonify({
        "total":len(resultado),
        "pacientes":resultado
    }), 200


@pacientes_bp.route(
    "/api/pacientes/<int:paciente_id>",
    methods=["GET"]
)
@login_required
def buscar_paciente(paciente_id):
    paciente = db.session.get(Paciente, paciente_id)

    if paciente is None:

        return jsonify({
            "erro":"Paciente nao encontrado."
        }), 404

    return jsonify({
        "paciente":{
            "id": paciente.id,
            "nome":paciente.nome,
            "data_nascimento": paciente.data_nascimento.isoformat(),
            "sexo":paciente.sexo
        }
    }), 200

@pacientes_bp.route("/api/pacientes/<int:paciente_id>",methods=["PATCH"])
@login_required
def atualizar_paciente(paciente_id):

    paciente = db.session.get(Paciente,paciente_id)

    if paciente is None:
        return jsonify({
            "erro":"Paciente nao encontrado."

        }), 404
    dados = request.get_json(silent=True)

    if not isinstance(dados,dict) or not dados:
        return jsonify({
            "erro: Envie um JSON valido com dados para atualiar."
        }), 400

    campos_permitidos = {"nome","data_nascimento","sexo"}

    if not set(dados).issubset(campos_permitidos):
        return jsonify({
            "erro":"Existem campos nao permitidos."
        }), 400

    if "nome" in dados:
        nome = dados["nome"]
        if not isinstance(nome,str) or not nome.strip():
            return jsonify({"erro":"Nome invalido."}),400
        paciente.nome = nome.strip()
    if "sexo" in dados:
        if dados["sexo"] not in ("masculino","feminino"):
            return jsonify({"erro":"Sexo invalido."}),400
        paciente.sexo=dados["sexo"]

    if "data_nascimento" in dados:
        from datetime import date

        try:
            paciente.data_nascimento = date.fromisoformat(
                dados["data_nascimento"]
            )
        except(ValueError,TypeError):
            return jsonify({
                "erro":"Data de nascimento invalida.Use AAA-MM-DD."
            }),400

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({
            "erro":"Nao foi possivel atualiar o paciente."
        }),500
    return jsonify({
        "mensagem":"Paciente atualizado com sucessso.",
        "paciente":{
            "id":paciente_id,
            "nome":paciente.nome,
            "data_nascimento":paciente.data_nascimento.isoformat(),
            "sexo":paciente.sexo
        }
    }),200

@pacientes_bp.route("/api/pacientes/<int:paciente_id>",methods=["DELETE"])
@login_required
def excluir_paciente(paciente_id):

    paciente = db.session.get(Paciente, paciente_id)

    if paciente is None:
        return jsonify({
            "erro":"Paciente nao encontrado."
        }), 404

    from models.avaliacao import Avaliacao

    possui_avaliacoes = Avaliacao.query.filter_by(
        paciente_id=paciente_id
    ).first()

    if possui_avaliacoes is not None:
        return jsonify({
            "erro":"Paciente possui avaliacoes vinculadas e nao pode sex excluido."
        }), 409

    try:
        db.session.delete(paciente)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({
            "erro":"Nao foi possivel excluir o paciente."
        }), 500

    return jsonify({
        "mensagem":"Paciente excluido com sucesso. "
    }), 200