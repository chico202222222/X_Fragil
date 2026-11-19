# Sistema de Triagem — Síndrome do X Frágil

Backend em **Flask** + banco **MySQL / TiDB Cloud**, servindo o front-end (`src/`) na mesma origem.

## 1. Instalar dependências

```bash
python -m venv .venv
```

Ative o ambiente virtual:
- **Windows (PowerShell):** `.\.venv\Scripts\Activate.ps1`
- **Linux/macOS:** `source .venv/bin/activate`

Instale os pacotes:
```bash
pip install -r requirements.txt
```

## 2. Configurar variáveis de ambiente

Copie o `.env.example` para `.env` na raiz do projeto e preencha os dados do banco:

```bash
cp .env.example .env
```

> Para **TiDB Cloud**, mantenha `DB_SSL="true"`. Para MySQL local, deixe `DB_SSL` fora ou `"false"`.

## 3. Preparar o banco (primeira vez)

```bash
cd backend-flask
flask --app app db upgrade
python scripts/popular_sintomas.py
python scripts/criar_admin.py
```

## 4. Rodar o servidor

```bash
cd backend-flask
python app.py
```

Acesse:
- Sistema: `http://127.0.0.1:5000`
- Teste de conexão com o banco: `http://127.0.0.1:5000/api/teste-banco`

## 5. Rodar os testes

Na raiz do projeto:
```bash
pytest backend-flask
```

*(O `test_score.py` roda sem banco; o `test_api.py` espera dados de teste criados por `backend-flask/scripts/popular_dados_teste.py` em um banco de testes.)*

## 6. Deploy em produção (Render / Railway)

- **Build:** `pip install -r requirements.txt && pip install gunicorn`
- **Start:** `gunicorn --chdir backend-flask --workers 1 --threads 4 --bind 0.0.0.0:$PORT app:app`
- **Variáveis de ambiente na hospedagem:** `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_SSL=true`, `COOKIE_SECURE=true` e uma `SECRET_KEY` forte.
