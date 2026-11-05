import {
  listarPacientes,
  criarPaciente,
  atualizarPaciente,
  excluirPaciente,
} from '../js/dto.js';

const form = document.querySelector('#form-paciente');
const inputNome = document.querySelector('#nome');
const inputNascimento = document.querySelector('#nascimento');
const selectSexo = document.querySelector('#sexo');
const botaoCancelar = document.querySelector('#cancelar');
const titulo = document.querySelector('#titulo-form');
const mensagem = document.querySelector('#mensagem');
const corpoTabela = document.querySelector('#pacientes-body');

// guarda o id do paciente que esta sendo editado (null = cadastrando)
let idEditando = null;

function mostrarMensagem(texto, ehErro) {
  mensagem.textContent = texto;
  if (ehErro) {
    mensagem.className = 'msg-erro';
  } else {
    mensagem.className = 'msg-ok';
  }
}

// 2015-05-20 vira 20/05/2015
function formatarData(data) {
  return data.split('-').reverse().join('/');
}

function textoSexo(sexo) {
  if (sexo === 'masculino') {
    return 'Masculino';
  }
  return 'Feminino';
}

function limparFormulario() {
  form.reset();
  idEditando = null;
  titulo.textContent = 'Cadastrar paciente';
  botaoCancelar.hidden = true;
}

function editar(paciente) {
  idEditando = paciente.id;
  inputNome.value = paciente.nome;
  inputNascimento.value = paciente.data_nascimento;
  selectSexo.value = paciente.sexo;
  titulo.textContent = 'Editar paciente';
  botaoCancelar.hidden = false;
  mensagem.textContent = '';
  inputNome.focus();
}

async function excluir(paciente) {
  if (!window.confirm('Excluir o paciente ' + paciente.nome + '?')) {
    return;
  }

  try {
    await excluirPaciente(paciente.id);
    mostrarMensagem('Paciente excluído.', false);
    carregarPacientes();
  } catch (error) {
    // 409 = paciente ja tem avaliacao
    mostrarMensagem(error.message, true);
  }
}

function criarBotao(texto, aoClicar) {
  const botao = document.createElement('button');
  botao.type = 'button';
  botao.className = 'button-secondary';
  botao.textContent = texto;
  botao.addEventListener('click', aoClicar);
  return botao;
}

function mostrarTabela(pacientes) {
  corpoTabela.replaceChildren();

  if (pacientes.length === 0) {
    const celula = corpoTabela.insertRow().insertCell();
    celula.colSpan = 4;
    celula.textContent = 'Nenhum paciente cadastrado ainda.';
    return;
  }

  pacientes.forEach((paciente) => {
    const linha = corpoTabela.insertRow();
    linha.insertCell().textContent = paciente.nome;
    linha.insertCell().textContent = formatarData(paciente.data_nascimento);
    linha.insertCell().textContent = textoSexo(paciente.sexo);

    const celulaAcoes = linha.insertCell();
    celulaAcoes.className = 'acoes';

    const linkAvaliar = document.createElement('a');
    linkAvaliar.href = '../avaliacoes/avaliacoes.html?paciente=' + paciente.id;
    linkAvaliar.className = 'link-avaliar';
    linkAvaliar.textContent = 'Avaliar';

    celulaAcoes.append(
      linkAvaliar,
      criarBotao('Editar', () => editar(paciente)),
      criarBotao('Excluir', () => excluir(paciente)),
    );
  });
}

async function carregarPacientes() {
  try {
    const pacientes = await listarPacientes();
    mostrarTabela(pacientes);
  } catch (error) {
    console.error(error);
    corpoTabela.replaceChildren();
    const celula = corpoTabela.insertRow().insertCell();
    celula.colSpan = 4;
    celula.textContent = 'Não foi possível carregar os pacientes.';
  }
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  mensagem.textContent = '';

  const dados = {
    nome: inputNome.value.trim(),
    data_nascimento: inputNascimento.value,
    sexo: selectSexo.value,
  };

  if (dados.nome === '') {
    mostrarMensagem('Informe o nome do paciente.', true);
    return;
  }

  try {
    if (idEditando === null) {
      await criarPaciente(dados);
      mostrarMensagem('Paciente cadastrado com sucesso.', false);
    } else {
      await atualizarPaciente(idEditando, dados);
      mostrarMensagem('Paciente atualizado com sucesso.', false);
    }
    limparFormulario();
    carregarPacientes();
  } catch (error) {
    mostrarMensagem(error.message, true);
  }
});

botaoCancelar.addEventListener('click', () => {
  limparFormulario();
  mensagem.textContent = '';
});

carregarPacientes();
