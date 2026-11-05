import { listarAvaliacoes } from '../js/dto.js';
import { exportToPDF } from '../js/pdf-export.js';

const corpoTabela = document.querySelector('#avaliacoes-body');
const inputDataInicial = document.querySelector('#data-inicial');
const inputDataFinal = document.querySelector('#data-final');
const selectPaciente = document.querySelector('#filtro-paciente');

let todasAvaliacoes = [];

function criarCelula(linha, classe, texto) {
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

// 2024-05-20 vira 20/05/2024
function formatarData(data) {
  return data.slice(0, 10).split('-').reverse().join('/');
}

// 20/05/2024 vira 2024-05-20 (devolve '' se estiver errado)
function converterData(texto) {
  const partes = texto.split('/');
  if (partes.length !== 3) {
    return '';
  }
  return partes[2] + '-' + partes[1] + '-' + partes[0];
}

function mostrarTabela(avaliacoes) {
  corpoTabela.replaceChildren();

  if (avaliacoes.length === 0) {
    mostrarMensagem('Nenhuma avaliação encontrada.');
    return;
  }

  avaliacoes.forEach((avaliacao) => {
    const linha = corpoTabela.insertRow();

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'avaliacao-checkbox';
    checkbox.setAttribute('aria-label', 'Selecionar avaliação de ' + avaliacao.paciente);
    linha.insertCell().append(checkbox);

    let score = '—';
    if (avaliacao.pontuacao !== null) {
      score = avaliacao.pontuacao.toLocaleString('pt-BR');
    }

    let resultado = '—';
    if (avaliacao.resultado) {
      resultado = avaliacao.resultado;
    }

    criarCelula(linha, 'paciente', avaliacao.paciente);
    criarCelula(linha, 'data', formatarData(avaliacao.data_avaliacao));
    criarCelula(linha, 'score', score);
    criarCelula(linha, 'resultado', resultado);
  });
}

// coloca os nomes dos pacientes no select de filtro
function preencherSelect() {
  const nomes = [];
  todasAvaliacoes.forEach((avaliacao) => {
    if (!nomes.includes(avaliacao.paciente)) {
      nomes.push(avaliacao.paciente);
    }
  });

  nomes.forEach((nome) => {
    const opcao = document.createElement('option');
    opcao.value = nome;
    opcao.textContent = nome;
    selectPaciente.append(opcao);
  });
}

function filtrar() {
  const dataInicial = converterData(inputDataInicial.value.trim());
  const dataFinal = converterData(inputDataFinal.value.trim());

  if (inputDataInicial.value.trim() !== '' && dataInicial === '') {
    window.alert('Use a data no formato DD/MM/AAAA');
    return;
  }

  if (inputDataFinal.value.trim() !== '' && dataFinal === '') {
    window.alert('Use a data no formato DD/MM/AAAA');
    return;
  }

  const filtradas = todasAvaliacoes.filter((avaliacao) => {
    const data = avaliacao.data_avaliacao.slice(0, 10);

    if (dataInicial !== '' && data < dataInicial) {
      return false;
    }
    if (dataFinal !== '' && data > dataFinal) {
      return false;
    }
    if (selectPaciente.value !== '' && avaliacao.paciente !== selectPaciente.value) {
      return false;
    }
    return true;
  });

  mostrarTabela(filtradas);
}

async function carregarAvaliacoes() {
  try {
    todasAvaliacoes = await listarAvaliacoes();
    preencherSelect();
    mostrarTabela(todasAvaliacoes);
  } catch (error) {
    console.error(error);
    mostrarMensagem('Não foi possível carregar as avaliações.');
  }
}

document.querySelector('#filtrar').addEventListener('click', filtrar);
document.querySelector('#exportar-pdf').addEventListener('click', exportToPDF);
document.querySelector('#imprimir').addEventListener('click', () => window.print());

// botao "limpar filtros" (reset do form): mostra tudo de novo
document.querySelector('.filters').addEventListener('reset', () => {
  mostrarTabela(todasAvaliacoes);
});

carregarAvaliacoes();
