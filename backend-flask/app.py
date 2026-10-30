"""Ponto de entrada da API do Sistema X Frágil."""
from flask import Flask, jsonify
from sqlalchemy import text

from config import Config
from database import db, migrate

# Importar os modelos permite que o SQLAlchemy reconheça as tabelas.
from models.usuario import Usuario
from models.paciente import Paciente
from models.avaliacao import Avaliacao
from models.sintoma import Sintoma
from models.resposta import Resposta

from routes.sintomas import sintomas_bp
from routes.pacientes import pacientes_bp
from routes.avaliacoes import avaliacoes_bp
from routes.respostas import respostas_bp
from routes.usuarios import usuarios_bp
from routes.auth import auth_bp

from limiter import limiter
from csrf_utils import csrf_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
limiter.init_app(app)

# Cada grupo de rotas cuida de uma parte do sistema.
for grupo in (sintomas_bp, pacientes_bp, avaliacoes_bp,
              respostas_bp, usuarios_bp, auth_bp,csrf_bp):
    app.register_blueprint(grupo)


@app.get("/")
def inicio():
    return jsonify({"mensagem": "API do Sistema de Triagem do X Frágil"})


@app.get("/api/teste-banco")
def testar_banco():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "sucesso", "mensagem": "MySQL conectado"})
    except Exception:
        app.logger.exception("Falha ao conectar ao MySQL")
        return jsonify({"status": "erro", "mensagem": "Erro de conexão com o banco"}), 500


if __name__ == "__main__":
    app.run(debug=False)
