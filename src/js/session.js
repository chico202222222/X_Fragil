// esse arquivo roda em todas as telas de dentro do sistema
// confere se tem usuario logado e liga o botao de sair
import { sessao, logout } from './dto.js';

async function sair(event) {
  event.preventDefault();
  try {
    await logout();
  } catch (error) {
    console.error('Erro ao sair:', error);
  }
  window.location.href = '../login/login.html';
}

async function mostrarUsuario() {
  try {
    const dados = await sessao();
    document.querySelector('#nome-usuario').textContent = 'Olá, ' + dados.usuario.nome;
  } catch (error) {
    // sem sessao, manda pro login
    window.location.href = '../login/login.html';
  }
}

document.querySelector('.logout').addEventListener('click', sair);
mostrarUsuario();
