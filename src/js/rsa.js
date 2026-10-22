const algoritmo = { name: 'RSA-OAEP', hash: 'SHA-256' };

function paraBase64(bytes) {
  return btoa(String.fromCharCode(...bytes));
}

function deBase64(texto) {
  return Uint8Array.from(atob(texto), caractere => caractere.charCodeAt(0));
}

// Gere e guarde a chave privada apenas no backend.
async function gerarParDeChaves() {
  const chaves = await crypto.subtle.generateKey(
    {
      name: 'RSA-OAEP',
      hash: 'SHA-256',
      modulusLength: 2048,
      publicExponent: new Uint8Array([1, 0, 1]),
    },
    true,
    ['encrypt', 'decrypt']
  );

  const chavePublica = await crypto.subtle.exportKey('jwk', chaves.publicKey);
  const chavePrivada = await crypto.subtle.exportKey('jwk', chaves.privateKey);

  return { chavePublica, chavePrivada };
}

async function criptografar(texto, chavePublica) {
  const chave = await crypto.subtle.importKey('jwk', chavePublica, algoritmo, false, ['encrypt']);
  const dados = new TextEncoder().encode(texto);
  const resultado = await crypto.subtle.encrypt(algoritmo, chave, dados);

  return paraBase64(new Uint8Array(resultado));
}

async function descriptografar(texto, chavePrivada) {
  const chave = await crypto.subtle.importKey('jwk', chavePrivada, algoritmo, false, ['decrypt']);
  const dados = deBase64(texto);
  const resultado = await crypto.subtle.decrypt(algoritmo, chave, dados);

  return new TextDecoder().decode(resultado);
}

window.Rsa = { gerarParDeChaves, criptografar, descriptografar };
