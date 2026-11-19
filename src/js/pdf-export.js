// pega as linhas marcadas na tabela (ou uma avaliacao com sintomas) e gera o pdf
// o jspdf e carregado pelo html (window.jspdf)
import { listarRespostas } from './dto.js';

function gerarPdfAvaliacoes(avaliacoes, nomeArquivo) {
  if (!window.jspdf || !window.jspdf.jsPDF) {
    window.alert('Biblioteca de PDF não carregada. Verifique sua conexão e tente novamente.');
    return;
  }

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();
  const alturaPagina = doc.internal.pageSize.getHeight();
  const larguraTexto = doc.internal.pageSize.getWidth() - 20;
  let posicaoY = 20;

  function garantirEspaco(alturaNecessaria) {
    if (posicaoY + alturaNecessaria > alturaPagina - 15) {
      doc.addPage();
      posicaoY = 20;
    }
  }

  doc.setFontSize(16);
  doc.text('Resultado da Triagem X-Frágil', 10, posicaoY);
  doc.setFontSize(11);
  posicaoY += 15;

  avaliacoes.forEach((avaliacao) => {
    garantirEspaco(38);

    doc.text('Paciente: ' + avaliacao.paciente, 10, posicaoY);
    doc.text('Data: ' + avaliacao.data, 10, posicaoY + 7);
    doc.text('Score: ' + avaliacao.score, 10, posicaoY + 14);
    doc.text('Resultado: ' + avaliacao.resultado, 10, posicaoY + 21);
    posicaoY += 32;

    (avaliacao.sintomas ?? []).forEach((sintoma) => {
      const linhasDescricao = doc.splitTextToSize('Sintoma: ' + sintoma.descricao, larguraTexto);
      garantirEspaco(linhasDescricao.length * 6 + 10);
      doc.text(linhasDescricao, 10, posicaoY);
      posicaoY += linhasDescricao.length * 6;
      doc.text('Resposta: ' + sintoma.resposta, 10, posicaoY);
      posicaoY += 8;
    });

    posicaoY += 6;
  });

  doc.save(nomeArquivo);
}

export async function exportToPDF() {
  const selecionadas = Array.from(
    document.querySelectorAll('.avaliacao-checkbox:checked'),
    (checkbox) => {
      const linha = checkbox.closest('tr');
      return {
        id: checkbox.dataset.avaliacaoId,
        paciente: linha.querySelector('.paciente').textContent.trim(),
        data: linha.querySelector('.data').textContent.trim(),
        score: linha.querySelector('.score').textContent.trim(),
        resultado: linha.querySelector('.resultado').textContent.trim(),
      };
    },
  );

  if (selecionadas.length === 0) {
    window.alert('Selecione pelo menos uma avaliação para exportar.');
    return;
  }

  const avaliacoes = await Promise.all(
    selecionadas.map(async (avaliacao) => {
      if (!avaliacao.id) return avaliacao;
      try {
        const respostas = await listarRespostas(avaliacao.id);
        return {
          ...avaliacao,
          sintomas: respostas.map((r) => ({
            descricao: r.descricao,
            resposta: r.presente ? 'Sim' : 'Não',
          })),
        };
      } catch {
        return avaliacao;
      }
    }),
  );

  gerarPdfAvaliacoes(avaliacoes, 'relatorio-avaliacoes.pdf');
}

export function exportAvaliacaoToPDF(avaliacao) {
  gerarPdfAvaliacoes([avaliacao], 'avaliacao-sintomas.pdf');
}
