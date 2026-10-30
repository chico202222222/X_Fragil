#configuacao do interpretador
import sys
#configura caminho
from pathlib import Path

SISTEMA_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SISTEMA_DIR))

from app import app
from database import db
from models.sintoma import Sintoma


SINTOMAS = [
    ("Atraso na fala", "ambos"),
    ("Dificuldades de aprendizagem", "ambos"),
    ("Déficit de atenção", "ambos"),
    ("Deficiência intelectual", "ambos"),
    ("Hiperatividade", "ambos"),
    ("Agressividade", "ambos"),
    ("Evita contato físico", "ambos"),
    ("Evita contato visual", "ambos"),
    ("Movimentos intencionais, repetitivos e rítmicos", "ambos"),
    ("Hipermobilidade articular", "ambos"),
    ("Macroorquidismo", "masculino"),
    ("Face alongada, mandíbula proeminente e/ou orelhas salientes", "ambos")
]


def popular_sintomas():
    with app.app_context():
        adicionados = 0

        for descricao, sexo in SINTOMAS:
            existente = Sintoma.query.filter_by(descricao=descricao).first()

            if existente is None:
                sintoma = Sintoma(
                    descricao=descricao,
                    sexo_aplicavel=sexo,
                    peso=1.0,
                    ativo=True
                )

                db.session.add(sintoma)
                adicionados += 1

        db.session.commit()

        total = Sintoma.query.count()

        print(f"Sintomas adicionados: {adicionados}")
        print(f"Total de sintomas no banco: {total}")


if __name__ == "__main__":
    popular_sintomas()
