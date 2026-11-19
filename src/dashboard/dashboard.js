import { listarPacientes, listarAvaliacoes } from '../js/dto.js';

// mostra o numero no card (troca o "—" pelo valor)
function mostrar(id, valor) {
  document.querySelector('#' + id).textContent = valor; // isso aqui automatiza a troca do "—" pelo valor, sem precisar ficar fazendo if pra cada card
}

// formatar o tempo
function formatarData(data) {
  return data.slice(0, 10).split('-').reverse().join('/'); // isso foi chato, tive que buscar no stackoverflow
}

// confere se a avaliacao foi feita no mes e ano atuais
function doMesAtual(data) {
  const agora = new Date();
  const dataAvaliacao = new Date(data);
  return dataAvaliacao.getMonth() === agora.getMonth() &&
    dataAvaliacao.getFullYear() === agora.getFullYear();
}

function mostrarUltimas(avaliacoes) {
  const corpo = document.querySelector('#ultimas-body');
  corpo.replaceChildren();

  if (avaliacoes.length === 0) {
    const celula = corpo.insertRow().insertCell();
    celula.colSpan = 3;
    celula.textContent = 'Nenhuma avaliação ainda.';
    return;
  }

  // as 5 mais recentes (a API ja manda da mais nova pra mais antiga)
  avaliacoes.slice(0, 5).forEach((avaliacao) => {
    const linha = corpo.insertRow();
    linha.insertCell().textContent = avaliacao.paciente;
    linha.insertCell().textContent = formatarData(avaliacao.data_avaliacao);

    let score = '—';
    if (avaliacao.pontuacao !== null) {
      score = avaliacao.pontuacao.toLocaleString('pt-BR');
    }
    linha.insertCell().textContent = score;
  });
}

async function carregarDashboard() {
  try {
    const [pacientes, avaliacoes] = await Promise.all([
      listarPacientes(),
      listarAvaliacoes(),
    ]);

    mostrar('total-pacientes', pacientes.length);
    mostrar('total-avaliacoes', avaliacoes.length);

    const doMes = avaliacoes.filter((a) => doMesAtual(a.data_avaliacao));
    // o filter aqui usa a funcao doMesAtual p filtrar e criar uma nova lista a partir da lista original, mantendo as novas avaliacoes que satisfazem a nova condicao imposta.
    mostrar('avaliacoes-mes', doMes.length);

    // score medio so entra quem tem pontuacao
    const comScore = avaliacoes.filter((a) => a.pontuacao !== null);
    if (comScore.length > 0) {
      const soma = comScore.reduce((total, a) => total + a.pontuacao, 0);
      const media = soma / comScore.length;
      mostrar('score-medio', media.toLocaleString('pt-BR', { maximumFractionDigits: 2 }));
    }

    mostrarUltimas(avaliacoes);
  } catch (error) {
    console.error(error);
    const corpo = document.querySelector('#ultimas-body');
    corpo.replaceChildren();
    const celula = corpo.insertRow().insertCell();
    celula.colSpan = 3;
    celula.textContent = 'Não foi possível carregar o dashboard.';
  }
}

carregarDashboard();
