from database import db

class Sintoma(db.Model):
    __tablename__ = "sintomas"

    id = db.Column(db.Integer, primary_key=True)

    descricao = db.Column(
        db.String(255),
        nullable=False
    )

    peso = db.Column(
        db.Float,
        nullable=False,
        default = 1.0
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    sexo_aplicavel = db.Column(
        db.String(10),
        nullable=False
    )
