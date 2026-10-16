import { validateLogin } from './validacaoCampos.js';

const form = document.getElementById('login-form');
const erro = document.getElementById('msgerro');

async function enviarLogin(credentials) {
  const res = await fetch('/api/login', {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  });

  const body = await res.json().catch(() => ({}));
  return { ok: res.ok, status: res.status, body };
}

fetch('/api/sessao', { credentials: 'include' }).then((res) => {
  if (res.ok) {
    window.location.href = '../home/home.html';
  }
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  erro.textContent = '';

  const validacao = validateLogin(form);
  if (validacao.error) {
    erro.textContent = validacao.error;
    return;
  }

  try {
    const result = await enviarLogin(validacao.data);

    if (result.status === 401) {
      erro.textContent = 'Usuário ou senha inválidos';
      return;
    }

    if (!result.ok) {
      const msg = result.body.error; // erro do corpo da resposta (descrição do erro)
      erro.textContent = msg;
      return;
    }
    window.location.href = '../home/home.html';
  } catch (error) {
    erro.textContent = 'Não foi possível conectar ao servidor';
    console.error(error);
  }
});
