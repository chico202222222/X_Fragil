async function limparSessao (event) {
  event.preventDefault()
  try {
    await fetch('/api/logout', { method: 'POST', credentials: 'include' })
    window.location.href = '../login/login.html'
  } catch (error) {
    console.error('Erro ao limpar sessão:', error)
  }
}


async function fetchSessao(){
 fetch('/api/sessao', { credentials: 'include' }).then(async res => {
  if (!res.ok) {
    window.location.href = '../login/login.html'
  } else {
    document.querySelector('#nome-usuario').textContent = 
    `Olá, ${(await res.json()).usuario.nome}`}})
  }

document.addEventListener('DOMContentLoaded', fetchSessao)
