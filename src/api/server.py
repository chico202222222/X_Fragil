import os

from flask import Flask

from login.route import registrar_rotas_login

SRC = os.path.join(os.path.dirname(__file__), '..')

app = Flask(__name__, static_folder=SRC, static_url_path='')

print('[server] criando rotas...')
registrar_rotas_login(app)
print('[server] pronto')

if __name__ == '__main__':
    print('[server] subindo em http://127.0.0.1:3456/login/login.html')
    app.run(host='127.0.0.1', port=3456, debug=True)
