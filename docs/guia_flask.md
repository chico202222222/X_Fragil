# guia flask 15/10/2026

servidor em src/api/server.py. rotas tipo login/route.py vao ser as rotas da api !

## subir

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def inicio():
    return 'oi'

app.run(host='127.0.0.1', port=3456, debug=True)
```

## rota post (como o login)

```python
from flask import request, jsonify

def login():
    dados = request.get_json(silent=True)
    if dados is None:
        dados = {}
    email = dados.get('email', '')
    return jsonify({'email': email})

app.add_url_rule('/api/login', view_func=login, methods=['POST'])
```

codigos: 200 ok, 201 criado, 400 errado, 401 nao logado.

## html css js

```python
import os
pasta = os.path.join(os.path.dirname(__file__), '..')
app = Flask(__name__, static_folder=pasta, static_url_path='')
```

abre http://127.0.0.1:3456/login/login.html

## sessao 24 horas (ainda nao fizemos)

```python
from datetime import timedelta
from flask import session

app.secret_key = 'mude-isso'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

session.permanent = True
session['user_id'] = usuario.id

user_id = session.get('user_id')
session.clear()  # logout
```

no fetch do front: credentials: 'include' pra mandar o cookie.
