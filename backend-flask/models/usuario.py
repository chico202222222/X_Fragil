from database import db

class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(
        db.String(120)
        , nullable=False
        )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable = False
        )

    senha_hash = db.Column(
        db.String(255),
        nullable=False
        )
    #define o tipo de perfil criado pelo usuario
    perfil = db.Column(
        db.String(20),
        nullable=False,
        default = "profissional",
        server_default = "profissional"
    )

    criado_em = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )
