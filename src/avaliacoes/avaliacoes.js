import {
  listarPacientes,
  listarSintomas,
  criarAvaliacao,
  enviarRespostas,
  historicoDoPaciente,
} from '../js/dto.js';

const form = document.querySelector('#form-avaliacao');
const selectPaciente = document.querySelector('#paciente');
const listaSintomas = document.querySelector('#lista-sintomas');
const botaoSalvar = document.querySelector('#salvar');
const mensagem = document.querySelector('#mensagem');
const caixaResultado = document.querySelector('#resultado');
const corpoHistorico = document.querySelector('#historico-body');

let pacientes = [];
let sintomas = [];

function mostrarMensagem(texto, ehErro) {
  mensagem.textContent = texto;
  if (ehErro) {
    mensagem.className = 'msg-erro';
  } else {
    mensagem.className = 'msg-ok';
  }
}

// cria um radio com o texto do lado
function criarOpcao(sintomaId, valor, texto) {
  const label = document.createElement('label');
  label.className = 'opcao';

  const radio = document.createElement('input');
  radio.type = 'radio';
  radio.name = 'sintoma-' + sintomaId;
  radio.value = valor;

  label.append(radio, ' ' + texto);
  return label;
}

function mostrarSintomas() {
  listaSintomas.replaceChildren();

  sintomas.forEach((sintoma) => {
    const linha = document.createElement('div');
    linha.className = 'sintoma';

    const descricao = document.createElement('span');
    descricao.textContent = sintoma.descricao;

    linha.append(
      descricao,
      criarOpcao(sintoma.id, 'sim', 'Sim'),
      criarOpcao(sintoma.id, 'nao', 'Não'),
    );
    listaSintomas.append(linha);
  });
}

function mostrarHistorico(avaliacoes) {
  corpoHistorico.replaceChildren();

  if (avaliacoes.length === 0) {
    const celula = corpoHistorico.insertRow().insertCell();
    celula.colSpan = 3;
    celula.textContent = 'Este paciente ainda não tem avaliações.';
    return;
  }

  avaliacoes.forEach((avaliacao) => {
    const linha = corpoHistorico.insertRow();
    linha.insertCell().textContent = avaliacao.data_avaliacao.slice(0, 10).split('-').reverse().join('/');

    if (avaliacao.pontuacao === null) {
      linha.insertCell().textContent = '—';
    } else {
      linha.insertCell().textContent = avaliacao.pontuacao.toLocaleString('pt-BR');
    }

    if (avaliacao.status === 'concluida') {
      linha.insertCell().textContent = 'Concluída';
    } else {
      linha.insertCell().textContent = 'Pendente';
    }
  });
}

async function carregarHistorico(pacienteId) {
  try {
    const avaliacoes = await historicoDoPaciente(pacienteId);
    mostrarHistorico(avaliacoes);
  } catch (error) {
    console.error(error);
    corpoHistorico.replaceChildren();
    const celula = corpoHistorico.insertRow().insertCell();
    celula.colSpan = 3;
    celula.textContent = 'Não foi possível carregar o histórico.';
  }
}

// quando escolhe um paciente carrega o checklist e o historico dele
async function escolherPaciente() {
  mensagem.textContent = '';
  caixaResultado.hidden = true;

  const paciente = pacientes.find((p) => String(p.id) === selectPaciente.value);

  if (!paciente) {
    sintomas = [];
    listaSintomas.replaceChildren();
    botaoSalvar.hidden = true;
    return;
  }

  try {
    // o checklist muda conforme o sexo do paciente
    sintomas = await listarSintomas(paciente.sexo);
    mostrarSintomas();
    botaoSalvar.hidden = false;
    carregarHistorico(paciente.id);
  } catch (error) {
    mostrarMensagem(error.message, true);
  }
}

// monta a lista de respostas, devolve null se faltar alguma
function pegarRespostas() {
  const respostas = [];

  for (const sintoma of sintomas) {
    const marcado = form.querySelector('input[name="sintoma-' + sintoma.id + '"]:checked');

    if (marcado === null) {
      return null;
    }

    respostas.push({
      sintoma_id: sintoma.id,
      presente: marcado.value === 'sim',
    });
  }

  return respostas;
}

function mostrarResultado(dados) {
  const resumo = dados.resumo;

  document.querySelector('#resultado-score').textContent =
    'Score: ' + dados.score.toLocaleString('pt-BR');
  document.querySelector('#resultado-resumo').textContent =
    'Sintomas presentes: ' + resumo.sintomas_presentes +
    ' de ' + resumo.total_sintomas;
  document.querySelector('#resultado-aviso').textContent = dados.aviso;

  caixaResultado.hidden = false;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  mensagem.textContent = '';
  caixaResultado.hidden = true;

  const respostas = pegarRespostas();
  if (respostas === null) {
    mostrarMensagem('Responda todos os sintomas antes de salvar.', true);
    return;
  }

  const pacienteId = Number(selectPaciente.value);
  botaoSalvar.disabled = true;

  try {
    const avaliacao = await criarAvaliacao(pacienteId);
    const dados = await enviarRespostas(avaliacao.id, respostas);

    mostrarMensagem('Avaliação salva com sucesso.', false);
    mostrarResultado(dados);
    mostrarSintomas(); // limpa as respostas marcadas
    carregarHistorico(pacienteId);
  } catch (error) {
    mostrarMensagem(error.message, true);
  }

  botaoSalvar.disabled = false;
});

selectPaciente.addEventListener('change', escolherPaciente);

async function iniciar() {
  try {
    pacientes = await listarPacientes();
  } catch (error) {
    mostrarMensagem('Não foi possível carregar os pacientes.', true);
    return;
  }

  pacientes.forEach((paciente) => {
    const opcao = document.createElement('option');
    opcao.value = paciente.id;
    opcao.textContent = paciente.nome;
    selectPaciente.append(opcao);
  });

  if (pacientes.length === 0) {
    mostrarMensagem('Cadastre um paciente antes de fazer uma avaliação.', true);
    return;
  }

  // vem da tela de pacientes: avaliacoes.html?paciente=3
  const idDaUrl = new URLSearchParams(window.location.search).get('paciente');
  if (idDaUrl) {
    selectPaciente.value = idDaUrl;
    escolherPaciente();
  }
}

iniciar();
