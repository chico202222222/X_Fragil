
from database import db


class Resposta(db.Model):
    __tablename__ = "respostas"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    avaliacao_id = db.Column(
        db.Integer,
        db.ForeignKey("avaliacoes.id"),
        nullable=False
    )

    sintoma_id = db.Column(
        db.Integer,
        db.ForeignKey("sintomas.id"),
        nullable=False
    )

    presente = db.Column(
        db.Boolean,
        nullable=False
    )

    avaliacao = db.relationship(
        "Avaliacao",
        backref="respostas"
    )

    sintoma = db.relationship(
        "Sintoma",
        backref="respostas"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "avaliacao_id",
            "sintoma_id",
            name="uq_resposta_avaliacao_sintoma"
        ),
    )
