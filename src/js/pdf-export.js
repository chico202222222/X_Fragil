import {jspdf} from "jspdf";

const corpoTabela = document.querySelector("#avaliacoes-body");

function criarCelula(linha, classe, texto) {
    // cria uma celula em html/css e adiciona a ela o texto passado como parametro 
  const celula = linha.insertCell();
  celula.className = classe;
  celula.textContent = texto;
}

function mostrarMensagem(mensagem) {
  corpoTabela.replaceChildren();
  const celula = corpoTabela.insertRow().insertCell();
  celula.colSpan = 5;
  celula.textContent = mensagem;
}

async function carregarAvaliacoes() {
  try {
    const resposta = await fetch("/api/avaliacoes", {
      credentials: "include",
    });

    if (!resposta.ok) throw new Error("Falha ao carregar avaliações");

    const { avaliacoes } = await resposta.json();
    corpoTabela.replaceChildren();

    if (avaliacoes.length === 0) {
      mostrarMensagem("Nenhuma avaliação encontrada.");
      return;
    }

    avaliacoes.forEach((avaliacao) => {
      const linha = corpoTabela.insertRow();
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.className = "avaliacao-checkbox";
      checkbox.setAttribute(
        "aria-label",
        `Selecionar avaliação de ${avaliacao.paciente}`,
      );
      linha.insertCell().append(checkbox);

      const data = avaliacao.data_avaliacao
        .slice(0, 10)
        .split("-")
        .reverse()
        .join("/");

      criarCelula(linha, "paciente", avaliacao.paciente);
      criarCelula(linha, "data", data);
      criarCelula(
        linha,
        "score",
        avaliacao.pontuacao?.toLocaleString("pt-BR") ?? "—",
      );
      criarCelula(linha, "resultado", avaliacao.resultado ?? "—");
    });
  } catch (erro) {
    console.error(erro);
    mostrarMensagem("Não foi possível carregar as avaliações.");
  }
}

function exportToPDF() {
  const avaliacoesSelecionadas = Array.from(
    document.querySelectorAll(".avaliacao-checkbox:checked"),
    (checkbox) => {
      const linha = checkbox.closest("tr");

      return {
        paciente: linha.querySelector(".paciente").textContent.trim(),
        data: linha.querySelector(".data").textContent.trim(),
        score: linha.querySelector(".score").textContent.trim(),
        resultado: linha.querySelector(".resultado").textContent.trim(),
      };
    },
  );

  if (avaliacoesSelecionadas.length === 0) {
    window.alert("Selecione pelo menos uma avaliação para exportar.");
    return;
  }

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();
  const alturaPagina = doc.internal.pageSize.getHeight();
  let posicaoY = 20;

  doc.setFontSize(16);
  doc.text("Resultado da Triagem X-Frágil", 10, posicaoY);
  doc.setFontSize(11);
  posicaoY += 15;

  avaliacoesSelecionadas.forEach((avaliacao) => {
    if (posicaoY + 38 > alturaPagina - 15) {
      doc.addPage();
      posicaoY = 20;
    }

    doc.text(`Paciente: ${avaliacao.paciente}`, 10, posicaoY);
    doc.text(`Data: ${avaliacao.data}`, 10, posicaoY + 7);
    doc.text(`Score: ${avaliacao.score}`, 10, posicaoY + 14);
    doc.text(`Resultado: ${avaliacao.resultado}`, 10, posicaoY + 21);
    posicaoY += 38;
  });

  doc.save("relatorio-avaliacoes.pdf");
}

document.querySelector("#exportar-pdf").addEventListener("click", exportToPDF);
carregarAvaliacoes();


export { exportToPDF }