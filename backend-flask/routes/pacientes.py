
from datetime import date
from auth_utils import login_required
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from flask import session

from database import db
from models.paciente import Paciente

pacientes_bp = Blueprint("pacientes",__name__)

#criar funcao para json
#tranfosrma dado em dicionario
def paciente_para_json(paciente):
    return {
        "id":paciente.id,
        "nome":paciente.nome,
        "data_nascimento":paciente.data_nascimento.isoformat(),
        "sexo":paciente.sexo
    }

#api de cadastrar pacinte
@pacientes_bp.route("/api/pacientes", methods=["POST"])
@login_required
def cadastrar_paciente():
    #pega dados do front no formato json
    dados = request.get_json(silent=True)
#validacao para vim um json
    if not isinstance(dados, dict):
        return jsonify({
            "erro":"Envie um JSON valido."
        }), 400
#coleta os dados
    nome = dados.get("nome")
    nascimento = dados.get("data_nascimento")
    sexo = dados.get("sexo")
#validacao para digita dados de forma certa
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
#variavel paciente recebe classe Paciente
    paciente = Paciente(
        nome=nome.strip(),
        data_nascimento=data_nascimento,
        sexo=sexo,
        usuario_id=session["usuario_id"]
    )
#tenta adicionar ao banco de dados
    try:
        db.session.add(paciente)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "erro": "Nao foi possivel cadastrar o paciente"
        }), 500
#se deu certo retorna um json com a resposta e o codigo 201
    return jsonify({
        "mensagem":"Paciente cadastrado com sucesso.",
        "paciente":paciente_para_json(paciente)
    }) , 201
# api de listar tbm necessita estar logado
@pacientes_bp.route("/api/pacientes", methods=["GET"])
@login_required
def listar_pacientes():
#utiliza uma query de consulta ao banco onde o usuario id tem que ser o mesmo da usuario session

    pacientes = Paciente.query.filter_by(usuario_id=session["usuario_id"]).all()

    resultado = [
        paciente_para_json(paciente)
        for paciente in pacientes
    ]

    return jsonify({
        "total":len(resultado),
        "pacientes":resultado
    }), 200

#api de buscar
@pacientes_bp.route("/api/pacientes/<int:paciente_id>",methods=["GET"])
@login_required
def buscar_paciente(paciente_id):
    paciente = Paciente.query.filter_by(id=paciente_id,usuario_id=session["usuario_id"]).first()

    if paciente is None:

        return jsonify({
            "erro":"Paciente nao encontrado."
        }), 404

    return jsonify({
        "paciente":paciente_para_json(paciente)
    }), 200

#atualizar dado do paciente api
@pacientes_bp.route("/api/pacientes/<int:paciente_id>",methods=["PATCH"])
@login_required
def atualizar_paciente(paciente_id):
#query que atualiza
    paciente = Paciente.query.filter_by(id=paciente_id,usuario_id=session["usuario_id"]).first()
#se paciente vazio da erro404
    if paciente is None:
        return jsonify({
            "erro": "Paciente nao encontrado."
        }), 404

    dados = request.get_json(silent=True)
    #se dados nao for um dicionario retorna erro
    if not isinstance(dados, dict) or not dados:
        return jsonify({
            "erro": "Envie um JSON valido com dados para atualizar."
        }), 400

    campos_permitidos = {
        "nome",
        "data_nascimento",
        "sexo"
    }
    #verifica se os dados estao no padrao e validos
    for campo in dados:
        if campo not in campos_permitidos:
            return jsonify({
                "erro": "Existem campos nao permitidos."
            }), 400

    # Primeiro valida todos os dados
    novos_dados = {}

    if "nome" in dados:
        nome = dados["nome"]

        if not isinstance(nome, str) or not nome.strip():
            return jsonify({"erro": "Nome invalido."}), 400

        novos_dados["nome"] = nome.strip()

    if "sexo" in dados:
        sexo = dados["sexo"]

        if not isinstance(sexo, str):
            return jsonify({"erro": "Sexo invalido."}), 400

        sexo = sexo.strip().lower()

        if sexo not in ("masculino", "feminino"):
            return jsonify({"erro": "Sexo invalido."}), 400

        novos_dados["sexo"] = sexo

    if "data_nascimento" in dados:
        try:
            nascimento = date.fromisoformat(
                dados["data_nascimento"]
            )
        except (ValueError, TypeError):
            return jsonify({
                "erro": "Data de nascimento invalida. Use AAAA-MM-DD."
            }), 400

        if nascimento > date.today():
            return jsonify({
                "erro": "Data de nascimento nao pode ser futura."
            }), 400

        novos_dados["data_nascimento"] = nascimento

    # Somente altera o paciente depois de validar tudo
    if "nome" in novos_dados:
        paciente.nome = novos_dados["nome"]

    if "sexo" in novos_dados:
        paciente.sexo = novos_dados["sexo"]

    if "data_nascimento" in novos_dados:
        paciente.data_nascimento = novos_dados["data_nascimento"]

    try:
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "erro": "Nao foi possivel atualizar o paciente."
        }), 500

    return jsonify({
        "mensagem": "Paciente atualizado com sucesso.",
        "paciente": paciente_para_json(paciente)
    }), 200

#api de excluir paciente
@pacientes_bp.route("/api/pacientes/<int:paciente_id>",methods=["DELETE"])
@login_required
def excluir_paciente(paciente_id):
    #query para excluir
    paciente = Paciente.query.filter_by(id=paciente_id,usuario_id=session["usuario_id"]).first()

    if paciente is None:
        return jsonify({
            "erro":"Paciente nao encontrado."
        }), 404
    #nao deixa excluir paciente que possui avaliacao
    from models.avaliacao import Avaliacao

    possui_avaliacoes = Avaliacao.query.filter_by(paciente_id=paciente_id).first()

    if possui_avaliacoes is not None:
        return jsonify({
            "erro":"Paciente possui avaliacoes vinculadas e nao pode ser excluido."
        }), 409

    try:
        db.session.delete(paciente)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "erro":"Nao foi possivel excluir o paciente."
        }), 500

    return jsonify({
        "mensagem":"Paciente excluido com sucesso. "
    }), 200
