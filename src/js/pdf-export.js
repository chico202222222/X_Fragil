// pega as linhas marcadas na tabela e gera o pdf
// o jspdf e carregado pelo html (window.jspdf)


export function exportToPDF() {
  const avaliacoesSelecionadas = Array.from(
    document.querySelectorAll('.avaliacao-checkbox:checked'),
    (checkbox) => {
      const linha = checkbox.closest('tr');

      return {
        paciente: linha.querySelector('.paciente').textContent.trim(),
        data: linha.querySelector('.data').textContent.trim(),
        score: linha.querySelector('.score').textContent.trim(),
        resultado: linha.querySelector('.resultado').textContent.trim(),
      };
    },
  );

  if (avaliacoesSelecionadas.length === 0) {
    window.alert('Selecione pelo menos uma avaliação para exportar.');
    return;
  }

  const { jsPDF } = window.jspdf; // import do jsPDF do objeto global window, decisao feita p n precisar instalar o jspdf via npm e ficar com dependencias desnecessarias e usando node
  const doc = new jsPDF();
  const alturaPagina = doc.internal.pageSize.getHeight();
  let posicaoY = 20;

  doc.setFontSize(16);
  doc.text('Resultado da Triagem X-Frágil', 10, posicaoY);
  doc.setFontSize(11);
  posicaoY += 15;

  avaliacoesSelecionadas.forEach((avaliacao) => {
    // se nao cabe na pagina, cria outra
    if (posicaoY + 38 > alturaPagina - 15) {
      doc.addPage();
      posicaoY = 20;
    }

    doc.text('Paciente: ' + avaliacao.paciente, 10, posicaoY);
    doc.text('Data: ' + avaliacao.data, 10, posicaoY + 7);
    doc.text('Score: ' + avaliacao.score, 10, posicaoY + 14);
    doc.text('Resultado: ' + avaliacao.resultado, 10, posicaoY + 21);
    posicaoY += 38;
    // a tabela nao traz sintomas (a API de listagem nao os envia), entao sem eles pula a parte
    (avaliacao.sintomas ?? []).forEach((sintoma) => { // operador ?? significa que se nao tiver uma coisa, pula p outra
      doc.text('Sintoma: ' + sintoma.descricao, 10, posicaoY);
      doc.text('Resposta: ' + sintoma.resposta, 10, posicaoY + 7);
      posicaoY += 14;
    });
    posicaoY += 5; // espaço entre avaliações


  });

  doc.save('relatorio-avaliacoes.pdf');
}
