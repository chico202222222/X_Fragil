function validateLogin(form) {
  const email = form.email.value;
  const senha = form.senha.value;

  if (!form.email.checkValidity()) {
    return { error: 'Email inválido' };
  }

  if (senha.length < 8 || senha.length > 255) {
    return { error: 'Senha precisa ter entre 8 e 255 caracteres' };
  }

  return { data: { email, senha } };
}

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
// res = response
fetch('/api/sessao', { credentials: 'include' }).then((res) => {
  if (res.ok) {
    window.location.href = '../home/home.html';
  }
});

form.addEventListener('submit', async (event) => { // o event é o evento que foi disparado pelo formulário
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
      if (result.body.error) {
        erro.textContent = result.body.error;
      } else {
        erro.textContent = 'Não foi possível conectar ao servidor';
      }
      return;
    }
    window.location.href = '../home/home.html';
  } catch (error) {
    erro.textContent = 'Não foi possível conectar ao servidor';
    console.error(error);
  }
});
