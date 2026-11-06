// funcoes que falam com a API do flask
// todas as telas usam esse arquivo pra chamar o backend
/* 
decidimos tirar o prisma do front-end 
*/


let csrfToken = null;

// pega o token csrf (precisa mandar ele em todo metodo que nao seja GET)
async function pegarCsrf() {
  if (csrfToken) {
    return csrfToken;
  }
  const resposta = await fetch('/api/csrf-token', { credentials: 'include' });
  const dados = await resposta.json();
  csrfToken = dados.csrf_token;
  return csrfToken;
}

// funcao base, todas as outras usam ela
async function chamarApi(metodo, url, corpo, tentouDeNovo) {
  const opcoes = {
    method: metodo,
    credentials: 'include',
    headers: {},
  };

  if (corpo) { // se receber um corpo, converte pra JSON pra poder mandar pro backend
    opcoes.headers['Content-Type'] = 'application/json';
    opcoes.body = JSON.stringify(corpo); 
  }

  if (metodo !== 'GET') {
    opcoes.headers['X-CSRF-Token'] = await pegarCsrf(); // o header do CSRF precisa ser enviado p todas as requisicoes que n sejam get (que alterem dados)
  }

  const resposta = await fetch(url, opcoes);
  const dados = await resposta.json().catch(() => ({})); 
  // faz o parse do JSON; se a resposta nao for JSON valido, o catch devolve um objeto vazio pra nao quebrar o codigo
  // token csrf pode ter vencido, pega outro e tenta uma vez
  if (resposta.status === 403 && !tentouDeNovo) {
    csrfToken = null;
    return chamarApi(metodo, url, corpo, true);
  }

  // 401 fora de /api/login e /api/sessao significa que a sessao acabou: volta pro login
  if (resposta.status === 401 && url !== '/api/login' && url !== '/api/sessao') {
    window.location.href = '/login/login.html';
  }

  if (!resposta.ok) {
    const erro = new Error(dados.erro || 'Erro no servidor');
    erro.status = resposta.status;
    throw erro;
  }

  return dados;
}

// ---------- login ----------

export async function login(email, senha) {
  const dados = await chamarApi('POST', '/api/login', { email, senha });
  // o login cria uma sessao nova, entao o token antigo nao vale mais
  csrfToken = null;
  return dados;
}

export async function logout() {
  await chamarApi('POST', '/api/logout', {});
  csrfToken = null;
}

export function sessao() {
  return chamarApi('GET', '/api/sessao');
}

// so administrador consegue cadastrar usuario
export function createUser(dados) {
  return chamarApi('POST', '/api/usuarios', dados);
}

// ---------- pacientes ----------

export async function listarPacientes() {
  const dados = await chamarApi('GET', '/api/pacientes');
  return dados.pacientes;
}

export async function criarPaciente(paciente) {
  const dados = await chamarApi('POST', '/api/pacientes', paciente);
  return dados.paciente;
}

export async function atualizarPaciente(id, paciente) {
  const dados = await chamarApi('PATCH', '/api/pacientes/' + id, paciente);
  return dados.paciente;
}

export function excluirPaciente(id) {
  return chamarApi('DELETE', '/api/pacientes/' + id);
}

// ---------- sintomas ----------

export async function listarSintomas(sexo) {
  const dados = await chamarApi('GET', '/api/sintomas?sexo=' + sexo);
  return dados.sintomas;
}

// ---------- avaliacoes ----------

export async function listarAvaliacoes() {
  const dados = await chamarApi('GET', '/api/avaliacoes');
  return dados.avaliacoes;
}

export async function historicoDoPaciente(pacienteId) {
  const dados = await chamarApi('GET', '/api/pacientes/' + pacienteId + '/avaliacoes');
  return dados.avaliacoes;
}

export async function criarAvaliacao(pacienteId) {
  const dados = await chamarApi('POST', '/api/avaliacoes', { paciente_id: pacienteId });
  return dados.avaliacao;
}

// respostas e uma lista assim: [{ sintoma_id: 1, presente: true }]
export function enviarRespostas(avaliacaoId, respostas) {
  return chamarApi('POST', '/api/avaliacoes/' + avaliacaoId + '/respostas', { respostas });
}
