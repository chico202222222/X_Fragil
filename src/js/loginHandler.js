import { validateLogin } from './validacaoCampos.js';

class LoginApi {
  static async authenticate(credentials) {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
    });

    const body = await res.json().catch(() => ({}));
    return { ok: res.ok, status: res.status, body };
  }
}

class LoginHandler {
  constructor(form, errorElement) {
    this.form = form;
    this.erro = errorElement;
  }

  init() {
    this.form.addEventListener('submit', (event) => this.handleSubmit(event));
  }

  clearError() {
    this.erro.textContent = '';
  }

  showError(message) {
    this.erro.textContent = message;
  }

  async handleSubmit(event) {
    event.preventDefault();
    this.clearError();

    const validacao = validateLogin(this.form);
    if (validacao.error) {
      this.showError(validacao.error);
      return;
    }

    try {
      const result = await LoginApi.authenticate(validacao.data);

      if (result.status === 401) {
        this.showError('Usuário ou senha inválidos');
        return;
      }

      if (!result.ok) {
        this.showError(result.body.error ?? 'Não foi possível conectar ao servidor');
        return;
      }

      window.location.href = '../home/home.html';
    } catch {
      this.showError('Não foi possível conectar ao servidor');
    }
  }
}

const form = document.querySelector('form');
const erro = document.querySelector('.error-message');

new LoginHandler(form, erro).init();
