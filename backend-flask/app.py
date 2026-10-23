from flask import Flask
from sqlalchemy import text

from config import Config
from database import db, migrate

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

app = Flask(__name__)

#carregando as configuracoes do mysql

app.config.from_object(Config)

#inicinaod os bancos e migracao

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(sintomas_bp)
app.register_blueprint(pacientes_bp)
app.register_blueprint(avaliacoes_bp)
app.register_blueprint(respostas_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def inicio():
    return {"Sistema de Triagem da Sindrome do X fragil"
    }


@app.route("/api/teste-banco")
def testar_banco():
    try:

        db.session.execute(text("SELECT 1"))

        return {
            "status": "sucesso",
            "mensagem":"Conexao com MySQl funcionando"
        }
    except Exception:
        app.logger.exception("Erro ao conectar ao banco")
        return {
            "status":"erro",
            "mensagem":"Nao foi possivel conectar ao banco"
        }, 500

if __name__ == "__main__":
    app.run(debug=False)