import flask

def logout():
    flask.session.clear()
    return flask.jsonify({'message': 'Sessão encerrada com sucesso'})

def registrar_rotas_logout(app):
    app.add_url_rule('/api/logout', 'logout', logout, methods=['POST'])