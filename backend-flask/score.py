import json

def calcular_resumo(respostas) -> json:


    total = len(respostas)

    presentes = sum(
        1 for resposta in respostas
        if resposta.presente is True
    )

    ausentes = total - presentes

    return json.dumps({
        "total_sintomas":total,
        "sintomas_presentes":presentes,
        "sintomas_ausentes":ausentes
    })