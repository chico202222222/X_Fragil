def calcular_resumo(respostas):


    total = len(respostas)

    presentes = sum(
        1 for resposta in respostas
        if resposta.presente is True
    )

    ausentes = total - presentes

    return{
        "total_sintomas":total,
        "sintomas_presentes":presentes,
        "sintomas_ausentes":ausentes
    }