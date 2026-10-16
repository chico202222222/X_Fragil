async function limparSessao(event) {
  event.preventDefault();
  await fetch('/api/logout', { method: 'POST', credentials: 'include' });
  window.location.href = '../login/login.html';
}

fetch('/api/sessao', { credentials: 'include' }).then((res) => {
  if (!res.ok) {
    window.location.href = '../login/login.html';
  }
});
