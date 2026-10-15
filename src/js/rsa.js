// Criptografa senha com RSA antes de mandar pro servidor.
// Chave pública: no front. Chave privada: só no backend.

const rsa = { name: 'RSA-OAEP', hash: 'SHA-256' };

const aoGerarChaves = {
  ...rsa,
  modulusLength: 2048,
  publicExponent: new Uint8Array([1, 0, 1]),
};

function paraBase64(bytes) {
  return btoa(String.fromCharCode(...bytes));
}

function deBase64(base64) {
  return Uint8Array.from(atob(base64), (c) => c.charCodeAt(0));
}

async function gerarParDeChaves() {
  const par = await crypto.subtle.generateKey(aoGerarChaves, true, ['encrypt', 'decrypt']);
  return {
    chavePublica: await crypto.subtle.exportKey('jwk', par.publicKey),
    chavePrivada: await crypto.subtle.exportKey('jwk', par.privateKey),
  };
}

async function criptografar(texto, chavePublica) {
  const chave = await crypto.subtle.importKey('jwk', chavePublica, rsa, false, ['encrypt']);
  const bytes = await crypto.subtle.encrypt(rsa, chave, new TextEncoder().encode(texto));
  return paraBase64(new Uint8Array(bytes));
}

async function descriptografar(base64, chavePrivada) {
  const chave = await crypto.subtle.importKey('jwk', chavePrivada, rsa, false, ['decrypt']);
  const bytes = await crypto.subtle.decrypt(rsa, chave, deBase64(base64));
  return new TextDecoder().decode(bytes);
}

window.Rsa = { gerarParDeChaves, criptografar, descriptografar };
