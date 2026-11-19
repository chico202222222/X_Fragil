"""Cria os dados que o test_api.py espera encontrar no banco.

Usar SOMENTE em um banco de teste, depois de:
    flask --app app db upgrade
    python scripts/popular_sintomas.py
    python scripts/criar_admin.py   (gera o usuario id 1)

O que o script garante:
    usuario 2  -> perfil profissional
    paciente 1 -> masculino, responsavel = usuario 1
    avaliacao 1 -> do paciente 1, com respostas para todo o checklist
    avaliacoes 2 a 5 -> do paciente 1, sem respostas
"""
import sys
from datetime import date
from pathlib import Path

import bcrypt

PASTA_BACKEND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PASTA_BACKEND))

from app import app
from database import db
from models.usuario import Usuario
from models.paciente import Paciente
from models.avaliacao import Avaliacao
from models.sintoma import Sintoma
from models.resposta import Resposta


def popular():
    with app.app_context():
        admin = db.session.get(Usuario, 1)
        if admin is None or admin.perfil != "administrador":
            print("O usuario id 1 precisa ser o administrador. Rode criar_admin.py antes.")
            return

        if Sintoma.query.count() == 0:
            print("Nao ha sintomas. Rode popular_sintomas.py antes.")
            return

        if db.session.get(Usuario, 2) is None:
            senha = bcrypt.hashpw(b"ProfissionalTeste123", bcrypt.gensalt()).decode()
            db.session.add(Usuario(
                id=2,
                nome="Profissional Teste",
                email="profissional@teste.local",
                senha_hash=senha,
                perfil="profissional",
            ))

        if db.session.get(Paciente, 1) is None:
            db.session.add(Paciente(
                id=1,
                nome="Paciente Teste",
                data_nascimento=date(2015, 3, 10),
                sexo="masculino",
                usuario_id=1,
            ))

        db.session.flush()

        for avaliacao_id in range(1, 6):
            if db.session.get(Avaliacao, avaliacao_id) is None:
                db.session.add(Avaliacao(id=avaliacao_id, paciente_id=1))

        db.session.flush()

        # A avaliacao 1 precisa estar respondida; a 2 precisa ficar vazia.
        if Resposta.query.filter_by(avaliacao_id=1).count() == 0:
            sintomas = Sintoma.query.filter(
                Sintoma.ativo.is_(True),
                Sintoma.sexo_aplicavel.in_(["ambos", "masculino"]),
            ).all()
            for sintoma in sintomas:
                db.session.add(Resposta(
                    avaliacao_id=1,
                    sintoma_id=sintoma.id,
                    presente=sintoma.id in (1, 3, 4),
                ))

        db.session.commit()

        print("Usuarios:", Usuario.query.count())
        print("Pacientes:", Paciente.query.count())
        print("Avaliacoes:", Avaliacao.query.count())
        print("Respostas da avaliacao 1:", Resposta.query.filter_by(avaliacao_id=1).count())


if __name__ == "__main__":
    popular()
