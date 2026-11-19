from database import db


class Avaliacao(db.Model):
    __tablename__ = "avaliacoes"

    id = db.Column(db.Integer, primary_key=True)

    paciente_id = db.Column(
        db.Integer,
        db.ForeignKey("pacientes.id"),
        nullable=False
    )

    data_avaliacao = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable= False
    )

    pontuacao = db.Column(
        db.Float,
        nullable=True
    )

    resultado = db.Column(
        db.String(50),
        nullable=True
    )

    paciente = db.relationship(
        "Paciente",
        backref="avaliacoes"
    )