
"""Calculo descritivo e score ponderado do questionario."""

PESOS = {
    1:  {"masculino": 0.14, "feminino": 0.01},
    2:  {"masculino": 0.18, "feminino": 0.28},
    3:  {"masculino": 0.17, "feminino": 0.12},
    4:  {"masculino": 0.32, "feminino": 0.20},
    5:  {"masculino": 0.12, "feminino": 0.04},
    6:  {"masculino": 0.01, "feminino": 0.02},
    7:  {"masculino": 0.04, "feminino": 0.07},
    8:  {"masculino": 0.06, "feminino": 0.08},
    9:  {"masculino": 0.17, "feminino": 0.05},
    10: {"masculino": 0.19, "feminino": 0.04},
    11: {"masculino": 0.26},
    12: {"masculino": 0.29, "feminino": 0.09}
}


def calcular_resumo(respostas):
    total = len(respostas)

    presentes = sum(
        1 for resposta in respostas
        if resposta.presente is True
    )

    return {
        "total_sintomas": total,
        "sintomas_presentes": presentes,
        "sintomas_ausentes": total - presentes
    }


def calcular_score(respostas, sexo):
    if sexo not in ("masculino", "feminino"):
        raise ValueError("Sexo invalido.")

    score = 0.0

    for resposta in respostas:
        pesos_sintoma = PESOS.get(resposta.sintoma_id)

        if pesos_sintoma is None or sexo not in pesos_sintoma:
            raise ValueError("Sintoma sem peso aplicavel.")

        if type(resposta.presente) is not bool:
            raise ValueError("Resposta invalida.")

        if resposta.presente:
            score += pesos_sintoma[sexo]

    return round(score, 2)
