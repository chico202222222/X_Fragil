async function getScore(){
    await fetch('backend-flask/score.py', {
        method: 'GET', // ler o resultado apenas. nao alterar dados
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            respostas: []
        })
    })


}