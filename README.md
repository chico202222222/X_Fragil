`npm install` → `npm run db:push` → `npm start` → http://localhost:3456/login/login.html

DTO/middleware em classes (`src/js/dto.js`, `src/js/middleware.js`). Validação Zod em `validacaoCampos.js`.
# X_Fragil

## configuração do ambiente

instale as dependências:

```sh
.venv/bin/python -m pip install -r requirements.txt
```

crie um `.env` na raiz do projeto. ele é carregado automaticamente e não deve ir para o git.
use este modelo no `.env.example`, sem colocar uma chave real nele:

```dotenv
SECRET_KEY=
APP_ENV=development
FLASK_DEBUG=0
```

gere uma chave localmente e coloque o resultado em `SECRET_KEY` no seu `.env`:

```sh
.venv/bin/python -c 'import secrets; print(secrets.token_hex(32))'
```

sem `SECRET_KEY`, o servidor não inicia. variáveis já definidas no ambiente têm prioridade sobre o `.env`.
`DATABASE_URL` também pode ser definida no `.env`, inclusive para a migração de senhas.

para iniciar em desenvolvimento:

```sh
.venv/bin/python src/api/server.py
```

em produção, use `APP_ENV=production`, HTTPS e um servidor WSGI, não o servidor de desenvolvimento do flask.
o modo de produção exige cookies de sessão via HTTPS e desativa o debug.
em desenvolvimento, use `FLASK_DEBUG=1` apenas quando precisar.
os cookies são `HttpOnly` e `SameSite=Lax` em todos os ambientes.
isso evita muita coisa 

use uma chave diferente por ambiente e guarde os segredos nas variáveis, ou no gerenciador de segredos da hospedagem (provavel q seja railway)
não coloque a chave no frontend!!! se ela vazar, troque-a; isso invalida os cookies de sessão antigos.
o bcrypt não usa essa chave: ela serve para assinar as sessões do flask.

## Senhas no backend Python

instale as dependências com `.venv/bin/python -m pip install -r requirements.txt`.
as senhas atribuídas ao modelo `User` são salvas como hash bcrypt, e o login verifica esse hash ..

```sh
.venv/bin/python src/api/migrar_senhas.py
```

p rodar os testes sem alterar o banco real:

```sh
.venv/bin/python -m unittest discover -s src/api -p test_senhas.py -v
```
