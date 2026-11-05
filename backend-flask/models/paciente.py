from database import db
from flask import session

class Paciente(db.Model):
    __tablename__ = "pacientes"


    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(120), nullable=False)

    data_nascimento = db.Column(db.Date, nullable=False)

    sexo = db.Column(db.String(10), nullable = False)

    # Profissional responsavel pelo paciente
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=True
    )

    criado_em = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False

    )