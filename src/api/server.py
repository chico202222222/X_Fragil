import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, redirect, session

from login.route import registrar_rotas_login

SRC = os.path.join(os.path.dirname(__file__), '..')
load_dotenv(os.path.join(SRC, '..', '.env'))

chave_secreta = os.environ.get('SECRET_KEY')
if not chave_secreta or not chave_secreta.strip():
    raise RuntimeError('defina SECRET_KEY no ambiente ou no .env antes de iniciar')

producao = os.environ.get('APP_ENV') == 'production'

app = Flask(__name__, static_folder=SRC, static_url_path='')
app.secret_key = chave_secreta
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = producao

print('[server] criando rotas...')
registrar_rotas_login(app)
print('[server] pronto')

@app.route('/')
def index():
    if session.get('user_id') is None:
        return redirect('/login/login.html')
    return redirect('/home/home.html')


if __name__ == '__main__':
    print('[server] subindo em http://127.0.0.1:3456/login/login.html')
    debug = not producao and os.environ.get('FLASK_DEBUG') == '1'
    app.run(host='127.0.0.1', port=3456, debug=debug)
