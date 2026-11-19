# Rodar o servidor com MySQL local (preview)

guia SIMPLES .

## 1. MySQL (Homebrew)
```bash
brew install mysql
brew services start mysql
mysql -uroot -e "
CREATE DATABASE xfragil CHARACTER SET utf8mb4;
CREATE USER 'xfragil_app'@'localhost' IDENTIFIED BY 'preview123';
GRANT ALL ON xfragil.* TO 'xfragil_app'@'localhost';
FLUSH PRIVILEGES;"
```

## 2. `.env` na raiz
```
DB_HOST="127.0.0.1"
DB_PORT="3306"
DB_NAME="xfragil"
DB_USER="xfragil_app"
DB_PASSWORD="preview123"
SECRET_KEY="qualquer-string"
```
Sem `DB_PASSWORD` ou `SECRET_KEY` o app n inicia.

## 3. Dependencias
```bash
source .venv/bin/activate
pip install -r requirements.txt
pip install python-dotenv cryptography
```
dotenv n ta no requirements.txt e nem cryptography, mas só copiar/colar que ta suave

## 4. Tabelas e sintomas
```bash
cd backend-flask
export FLASK_APP=app.py
flask db upgrade # (vai atualizar)
python scripts/popular_sintomas.py
```

## 5. Subir o servidor
```bash
python app.py
```
Abre em http://127.0.0.1:5000 (o Flask serve o front de `src/`).
Teste de conexao: http://127.0.0.1:5000/api/teste-banco

## Problemas comuns
- `Access denied`: `DB_PASSWORD` do `.env` diferente da senha do MySQL.
- `ModuleNotFoundError: dotenv`: falta `pip install python-dotenv`.
- p limpar tudo: `brew services stop mysql && brew uninstall mysql`.
8765res z