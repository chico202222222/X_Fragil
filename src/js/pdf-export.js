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

  const { jsPDF } = window.jspdf;
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
  });

  doc.save('relatorio-avaliacoes.pdf');
}
