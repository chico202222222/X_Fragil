from app import app
from database import db


def test_sintomas_sem_login():
    cliente = app.test_client()

    resposta = cliente.get(
        "/api/sintomas?sexo=masculino"
    )

    assert resposta.status_code == 401


def test_sintomas_com_login():
    cliente = app.test_client()

    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 2

    resposta = cliente.get(
        "/api/sintomas?sexo=masculino"
    )

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert dados["sexo"] == "masculino"
    assert dados["total"] == 12


def test_profissional_nao_acessa_paciente_de_outro():
    cliente = app.test_client()

    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 2

    resposta = cliente.get("/api/pacientes/1")

    assert resposta.status_code == 404

def test_profissional_nao_acessa_historico_de_outro():
    cliente = app.test_client()

    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 2

    resposta = cliente.get(
        "/api/pacientes/1/avaliacoes"
    )

    assert resposta.status_code == 404
def test_profissional_nao_acessa_respostas_de_outro():
    cliente = app.test_client()

    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 2

    resposta = cliente.get(
        "/api/avaliacoes/5/respostas"
    )

    assert resposta.status_code == 404

def test_profissional_nao_acessa_resumo_de_outro():
    cliente = app.test_client()

    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 2

    resposta = cliente.get(
        "/api/avaliacoes/5/resumo"
    )

    assert resposta.status_code == 404

def test_cadastrar_usuario_sem_login():
    cliente = app.test_client()

    #busca o token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #tenta cadastrar sem estar logado
    resposta = cliente.post(
        "/api/usuarios",
        json={
            "nome": "Teste",
            "email": "teste@example.com",
            "senha": "SenhaTeste123"
        },
        headers={"X-CSRF-Token": token}
    )

    assert resposta.status_code == 401

def test_profissional_nao_cadastra_usuario():
    cliente = app.test_client()

    #simula sessao de profissional
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 2

    #busca token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #tenta cadastrar outro usuario
    resposta = cliente.post(
        "/api/usuarios",
        json={
            "nome": "Teste",
            "email": "teste@example.com",
            "senha": "SenhaTeste123"
        },
        headers={"X-CSRF-Token": token}
    )

    assert resposta.status_code == 403

def test_administrador_acessa_cadastro():
    cliente = app.test_client()

    #simula sessao do administrador
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 1

    #busca token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #envia dados invalidos para nao cadastrar usuario
    resposta = cliente.post(
        "/api/usuarios",
        json={},
        headers={"X-CSRF-Token": token}
    )

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "Nome invalido."

def test_senha_bcrypt():
    import bcrypt
    from routes.auth import verificar_senha

    senha = "MinhaSenha12345"

    #gera hash bcrypt
    senha_hash = bcrypt.hashpw(
        senha.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    #verifica senha correta
    assert verificar_senha(senha, senha_hash) is True

    #verifica senha incorreta
    assert verificar_senha("SenhaErrada123", senha_hash) is False
def test_senha_werkzeug():
    from werkzeug.security import generate_password_hash
    from routes.auth import verificar_senha

    senha = "MinhaSenha12345"

    #gera hash com werkzeug
    senha_hash = generate_password_hash(senha)

    #verifica senha correta
    assert verificar_senha(senha, senha_hash) is True

    #verifica senha incorreta
    assert verificar_senha("SenhaErrada123", senha_hash) is False

def test_criar_avaliacao_sem_login():
    cliente = app.test_client()

    #busca token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #tenta criar avaliacao sem login
    resposta = cliente.post(
        "/api/avaliacoes",
        json={"paciente_id": 1},
        headers={"X-CSRF-Token": token}
    )

    assert resposta.status_code == 401

def test_criar_avaliacao_id_invalido():
    cliente = app.test_client()

    #simula login do profissional
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 2

    #busca token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #envia um id invalido
    resposta = cliente.post(
        "/api/avaliacoes",
        json={"paciente_id": -1},
        headers={"X-CSRF-Token": token}
    )

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "Informe um paciente_id inteiro positivo."


def test_criar_avaliacao_paciente_inexistente():
    cliente = app.test_client()

    #simula login do profissional
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 2

    #busca token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #tenta criar avaliacao para paciente inexistente
    resposta = cliente.post(
        "/api/avaliacoes",
        json={"paciente_id": 999999999},
        headers={"X-CSRF-Token": token}
    )

    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "Paciente nao encontrado."


def test_criar_avaliacao_json_invalido():
    cliente = app.test_client()

    #simula login do profissional
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 2

    #busca token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #envia um json no formato incorreto
    resposta = cliente.post(
        "/api/avaliacoes",
        json=[],
        headers={"X-CSRF-Token": token}
    )

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "Envie um Json valido."



def test_historico_paciente_inexistente():
    cliente = app.test_client()

    #simula login do profissional
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 2

    #busca historico de paciente inexistente
    resposta = cliente.get(
        "/api/pacientes/999999999/avaliacoes"
    )

    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "Paciente nao encontrado."


def test_resumo_sem_login():
    cliente = app.test_client()

    #tenta consultar resumo sem estar logado
    resposta = cliente.get(
        "/api/avaliacoes/5/resumo"
    )

    assert resposta.status_code == 401

def test_historico_paciente_valido():
    cliente = app.test_client()

    #simula sessao do usuario dono do paciente
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 1

    #consulta historico
    resposta = cliente.get(
        "/api/pacientes/1/avaliacoes"
    )

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert dados["paciente_id"] == 1
    assert isinstance(dados["avaliacoes"], list)
    assert dados["total"] == len(dados["avaliacoes"])

def test_resumo_avaliacao_inexistente():
    cliente = app.test_client()

    #simula login do administrador
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 1

    #consulta avaliacao inexistente
    resposta = cliente.get(
        "/api/avaliacoes/999999999/resumo"
    )

    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "Avaliacao nao encontrada."

def test_resumo_sem_respostas():
    cliente = app.test_client()

    #simula sessao do administrador
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 1

    #consulta avaliacao sem respostas
    resposta = cliente.get(
        "/api/avaliacoes/2/resumo"
    )

    assert resposta.status_code == 409
    assert resposta.get_json()["erro"] == "Esta avaliacao ainda nao possui respostas."


def test_registrar_respostas_sem_login():
    cliente = app.test_client()

    #busca token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #tenta registrar respostas sem login
    resposta = cliente.post(
        "/api/avaliacoes/2/respostas",
        json={"respostas": []},
        headers={"X-CSRF-Token": token}
    )

    assert resposta.status_code == 401

def test_registrar_respostas_json_invalido():
    cliente = app.test_client()

    #simula login do profissional
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 2

    #busca token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #envia json invalido para a rota
    resposta = cliente.post(
        "/api/avaliacoes/2/respostas",
        json=[],
        headers={"X-CSRF-Token": token}
    )

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "Envie um JSON valido."

def test_registrar_respostas_lista_invalida():
    cliente = app.test_client()

    #simula login do profissional
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 2

    #busca token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #envia respostas como texto em vez de lista
    resposta = cliente.post(
        "/api/avaliacoes/2/respostas",
        json={"respostas": "sim"},
        headers={"X-CSRF-Token": token}
    )

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "Informe uma lista de respostas."

def test_registrar_respostas_incompletas():
    cliente = app.test_client()

    #simula login do dono da avaliacao
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 1

    #busca token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #envia uma lista vazia de respostas
    resposta = cliente.post(
        "/api/avaliacoes/2/respostas",
        json={"respostas": []},
        headers={"X-CSRF-Token": token}
    )
    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "Envie uma resposta para cada sintoma do checklist."



def test_registrar_respostas_duplicadas():
    from models.paciente import Paciente
    from models.sintoma import Sintoma

    cliente = app.test_client()

    #simula login do dono da avaliacao
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 1

    #busca token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #busca os sintomas do checklist
    with app.app_context():
        paciente = Paciente.query.filter_by(id=1).first()

        sintomas = Sintoma.query.filter(
            Sintoma.ativo.is_(True),
            Sintoma.sexo_aplicavel.in_(["ambos", paciente.sexo])
        ).all()

        ids = [s.id for s in sintomas]

    assert len(ids) >= 2

    #monta respostas e repete um sintoma
    respostas = []

    for sintoma_id in ids:
        respostas.append({
            "sintoma_id": sintoma_id,
            "presente": False
        })

    respostas[-1]["sintoma_id"] = respostas[0]["sintoma_id"]

    #envia respostas duplicadas
    resposta = cliente.post(
        "/api/avaliacoes/2/respostas",
        json={"respostas": respostas},
        headers={"X-CSRF-Token": token}
    )

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "Sintoma duplicado na requisicao."

def test_registrar_respostas_sintoma_invalido():
    from models.paciente import Paciente
    from models.sintoma import Sintoma

    cliente = app.test_client()

    #simula login do dono da avaliacao
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 1

    #busca token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #busca os sintomas permitidos
    with app.app_context():
        paciente = Paciente.query.filter_by(id=1).first()

        sintomas = Sintoma.query.filter(
            Sintoma.ativo.is_(True),
            Sintoma.sexo_aplicavel.in_(["ambos", paciente.sexo])
        ).all()

        ids = [s.id for s in sintomas]
        id_invalido = max(
            [s.id for s in Sintoma.query.all()] + [0]
        ) + 1

    assert len(ids) > 0

    #monta o checklist com um id invalido
    respostas = []

    for sintoma_id in ids:
        respostas.append({
            "sintoma_id": sintoma_id,
            "presente": False
        })

    respostas[-1]["sintoma_id"] = id_invalido

    resposta = cliente.post(
        "/api/avaliacoes/2/respostas",
        json={"respostas": respostas},
        headers={"X-CSRF-Token": token}
    )

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "Sintoma nao pertence ao checklist."


def test_registrar_respostas_presente_invalido():
    from models.paciente import Paciente
    from models.sintoma import Sintoma

    cliente = app.test_client()

    #simula login do dono da avaliacao
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 1

    #busca token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #busca os sintomas permitidos
    with app.app_context():
        paciente = Paciente.query.filter_by(id=1).first()

        sintomas = Sintoma.query.filter(
            Sintoma.ativo.is_(True),
            Sintoma.sexo_aplicavel.in_(["ambos", paciente.sexo])
        ).all()

        ids = [s.id for s in sintomas]

    assert len(ids) > 0

    #monta o checklist
    respostas = []

    for sintoma_id in ids:
        respostas.append({
            "sintoma_id": sintoma_id,
            "presente": False
        })

    #coloca um valor invalido
    respostas[0]["presente"] = "sim"

    resposta = cliente.post(
        "/api/avaliacoes/2/respostas",
        json={"respostas": respostas},
        headers={"X-CSRF-Token": token}
    )

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "presente deve ser true ou false."

def test_registrar_respostas_id_tipo_invalido():
    from models.paciente import Paciente
    from models.sintoma import Sintoma

    cliente = app.test_client()

    #simula login do dono da avaliacao
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 1

    #busca token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #busca os sintomas permitidos
    with app.app_context():
        paciente = Paciente.query.filter_by(id=1).first()

        sintomas = Sintoma.query.filter(
            Sintoma.ativo.is_(True),
            Sintoma.sexo_aplicavel.in_(["ambos", paciente.sexo])
        ).all()

        ids = [s.id for s in sintomas]

    assert len(ids) > 0

    respostas = []

    for sintoma_id in ids:
        respostas.append({
            "sintoma_id": sintoma_id,
            "presente": False
        })

    #troca um ID inteiro por texto
    respostas[0]["sintoma_id"] = "invalido"

    resposta = cliente.post(
        "/api/avaliacoes/2/respostas",
        json={"respostas": respostas},
        headers={"X-CSRF-Token": token}
    )

    assert resposta.status_code == 400
    assert resposta.get_json()["erro"] == "sintoma_id invalido."

def test_avaliacao_ja_respondida():
    from models.paciente import Paciente
    from models.sintoma import Sintoma

    cliente = app.test_client()

    #simula login do dono da avaliacao
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 1

    #busca token csrf
    resposta_csrf = cliente.get("/api/csrf-token")
    token = resposta_csrf.get_json()["csrf_token"]

    #busca sintomas permitidos
    with app.app_context():
        paciente = Paciente.query.filter_by(id=1).first()

        sintomas = Sintoma.query.filter(
            Sintoma.ativo.is_(True),
            Sintoma.sexo_aplicavel.in_(["ambos", paciente.sexo])
        ).all()

        ids = [s.id for s in sintomas]

    assert len(ids) > 0

    #monta checklist completo
    respostas = []

    for sintoma_id in ids:
        respostas.append({
            "sintoma_id": sintoma_id,
            "presente": False
        })

    #tenta responder novamente a avaliacao 1
    resposta = cliente.post(
        "/api/avaliacoes/1/respostas",
        json={"respostas": respostas},
        headers={"X-CSRF-Token": token}
    )

    assert resposta.status_code == 409
    assert resposta.get_json()["erro"] == "Esta avaliacao ja possui respostas."

def test_listar_respostas_validas():
    cliente = app.test_client()

    #simula login do dono da avaliacao
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 1

    #consulta respostas da avaliacao
    resposta = cliente.get("/api/avaliacoes/1/respostas")

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert dados["avaliacao_id"] == 1
    assert isinstance(dados["respostas"], list)
    assert dados["total"] == len(dados["respostas"])
    assert dados["total"] > 0


def test_csrf_sem_token():
    cliente = app.test_client()

    #tenta realizar login sem token csrf
    resposta = cliente.post(
        "/api/login",
        json={
            "email": "teste@example.com",
            "senha": "SenhaTeste123"
        }
    )

    assert resposta.status_code == 403
    assert resposta.get_json()["erro"] == "Token CSRF ausente ou invalido."

from sqlalchemy import text


def test_gravacao_e_rollback():
    #abre uma conexao com o banco
    with app.app_context():
        conexao = db.engine.connect()
        transacao = conexao.begin()

        try:
            #cria um registro temporario dentro da transacao
            conexao.execute(
                text("""
                    INSERT INTO usuarios (nome, email, senha_hash, perfil)
                    VALUES (:nome, :email, :senha_hash, :perfil)
                """),
                {
                    "nome": "Teste Rollback",
                    "email": "rollback_teste@exemplo.invalid",
                    "senha_hash": "hash_teste",
                    "perfil": "profissional"
                }
            )

            #confirma que o registro existe dentro da transacao
            resultado = conexao.execute(
                text("""
                    SELECT COUNT(*)
                    FROM usuarios
                    WHERE email = :email
                """),
                {"email": "rollback_teste@exemplo.invalid"}
            ).scalar_one()

            assert resultado == 1

        finally:
            #desfaz a operacao, mesmo se o teste falhar
            transacao.rollback()
            conexao.close()

from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError


def test_rollback_cadastro_paciente():
    cliente = app.test_client()

    #simula usuario logado
    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = 1

    #pega token csrf
    token = cliente.get("/api/csrf-token").get_json()["csrf_token"]

    #simula erro ao salvar e acompanha o rollback
    with patch.object(db.session, "commit", side_effect=SQLAlchemyError("Erro simulado")):
        with patch.object(db.session, "rollback") as rollback:
            resposta = cliente.post(
                "/api/pacientes",
                json={
                    "nome": "Paciente Teste Rollback",
                    "data_nascimento": "2015-05-20",
                    "sexo": "masculino"
                },
                headers={"X-CSRF-Token": token}
            )

            assert resposta.status_code == 500
            rollback.assert_called_once()

def test_rollback_atualizacao_paciente():
    #ativa o contexto do Flask
    with app.app_context():
        cliente = app.test_client()

        #simula login do responsavel pelo paciente
        with cliente.session_transaction() as sessao:
            sessao["usuario_id"] = 1

        #obtem o token csrf
        token = cliente.get("/api/csrf-token").get_json()["csrf_token"]

        #simula uma falha ao salvar
        with patch.object(
            db.session,
            "commit",
            side_effect=SQLAlchemyError("Erro simulado")
        ):
            with patch.object(db.session, "rollback") as rollback:
                resposta = cliente.patch(
                    "/api/pacientes/1",
                    json={"nome": "Nome Temporario"},
                    headers={"X-CSRF-Token": token}
                )

                assert resposta.status_code == 500
                rollback.assert_called_once()

        #limpa a sessao dentro do contexto correto
        db.session.remove()

def test_rollback_exclusao_paciente():
    from unittest.mock import patch
    from sqlalchemy.exc import SQLAlchemyError
    from models.avaliacao import Avaliacao

    with app.app_context():
        cliente = app.test_client()

        #simula login do responsavel
        with cliente.session_transaction() as sessao:
            sessao["usuario_id"] = 1

        #pega o token csrf
        token = cliente.get("/api/csrf-token").get_json()["csrf_token"]

        #simula que nao existem avaliacoes vinculadas
        with patch.object(
            Avaliacao,
            "query"
        ) as consulta:

            consulta.filter_by.return_value.first.return_value = None

            #simula erro antes de excluir o paciente
            with patch.object(
                db.session,
                "delete",
                side_effect=SQLAlchemyError("Erro simulado")
            ):
                with patch.object(db.session, "rollback") as rollback:

                    resposta = cliente.delete(
                        "/api/pacientes/1",
                        headers={"X-CSRF-Token": token}
                    )

                    assert resposta.status_code == 500
                    rollback.assert_called_once()
