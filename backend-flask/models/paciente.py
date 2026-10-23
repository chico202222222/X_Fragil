from database import db

class Paciente(db.Model):
    __tablename__ = "pacientes"


    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(120), nullable=False)

    data_nascimento = db.Column(db.Date, nullable=False)

    sexo = db.Column(db.String(10), nullable = False)

    criado_em = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False

    )