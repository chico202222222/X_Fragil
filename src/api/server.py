import os
from datetime import timedelta

from flask import Flask, redirect, session

from login.route import registrar_rotas_login

SRC = os.path.join(os.path.dirname(__file__), '..')

app = Flask(__name__, static_folder=SRC, static_url_path='')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-mude-isso')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

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
    app.run(host='127.0.0.1', port=3456, debug=True)
