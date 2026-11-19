import { login, sessao } from './dto.js';

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

// se ja esta logado vai direto pra home
sessao()
  .then(() => {
    window.location.href = '../home/home.html';
  })
  .catch(() => {
    // 401 aqui e normal, so continua na tela de login
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
    await login(validacao.data.email, validacao.data.senha);
    window.location.href = '../home/home.html';
  } catch (error) {
    if (error.status === 401) {
      erro.textContent = 'Usuário ou senha inválidos';
    } else if (error.status === 429) {
      erro.textContent = 'Muitas tentativas, espere um minuto';
    } else if (error.status) {
      erro.textContent = error.message;
    } else {
      erro.textContent = 'Não foi possível conectar ao servidor';
      console.error(error);
    }
  }
});
