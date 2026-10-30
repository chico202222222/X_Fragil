import pytest
from types import SimpleNamespace

from score import calcular_score, calcular_resumo


def criar_resposta(sintoma_id, presente):
    return SimpleNamespace(
        sintoma_id=sintoma_id,
        presente=presente
    )


def test_score_masculino():
    respostas = [
        criar_resposta(1, True),
        criar_resposta(3, True),
        criar_resposta(4, True)
    ]

    assert calcular_score(respostas, "masculino") == 0.63


def test_score_feminino():
    respostas = [
        criar_resposta(1, True),
        criar_resposta(3, True),
        criar_resposta(4, True)
    ]

    assert calcular_score(respostas, "feminino") == 0.33


def test_resumo():
    respostas = [
        criar_resposta(1, True),
        criar_resposta(2, False),
        criar_resposta(3, True)
    ]

    assert calcular_resumo(respostas) == {
        "total_sintomas": 3,
        "sintomas_presentes": 2,
        "sintomas_ausentes": 1
    }



def test_sexo_invalido():
    respostas = [criar_resposta(1, True)]

    with pytest.raises(ValueError):
        calcular_score(respostas, "outro")


def test_sintoma_invalido():
    respostas = [criar_resposta(999, True)]

    with pytest.raises(ValueError):
        calcular_score(respostas, "masculino")


def test_macroorquidismo_feminino():
    respostas = [criar_resposta(11, True)]

    with pytest.raises(ValueError):
        calcular_score(respostas, "feminino")


def test_resposta_invalida():
    respostas = [criar_resposta(1, "sim")]

    with pytest.raises(ValueError):
        calcular_score(respostas, "masculino")


def test_nenhum_sintoma_presente():
    respostas = [
        criar_resposta(1, False),
        criar_resposta(2, False)
    ]

    assert calcular_score(respostas, "masculino") == 0.0
