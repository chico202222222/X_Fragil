import { validateRegister } from './validacaoCampos.js';
import { createUser } from './dto.js';

const form = document.querySelector('form');
const erro = document.querySelector('.error-message');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  erro.textContent = ''; // vazio, caso tenha algo so dar append

  const validacao = validateRegister(form);
  if (validacao.error) {
    erro.textContent = validacao.error;
    return;
  }

  try {
    const user = await createUser(validacao.data);
    if (!user) {
      erro.textContent = 'Usuário já existe';
      return;
    }
    window.location.href = '../home/home.html';
  } catch {
    erro.textContent = 'Não foi possível conectar ao servidor';
  }
});
