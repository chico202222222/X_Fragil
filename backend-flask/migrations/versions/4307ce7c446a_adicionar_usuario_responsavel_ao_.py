
"""Adicionar profissional responsável ao paciente.

Revision ID: 4307ce7c446a
Revises: e40baf2f95b0
"""

from alembic import op
import sqlalchemy as sa


revision = "4307ce7c446a"
down_revision = "e40baf2f95b0"
branch_labels = None
depends_on = None


def upgrade():
    # Adiciona o campo que identifica o profissional.
    op.add_column(
        "pacientes",
        sa.Column("usuario_id", sa.Integer(), nullable=True)
    )

    # Relaciona o paciente ao usuário responsável.
    op.create_foreign_key(
        "fk_pacientes_usuario_id",
        "pacientes",
        "usuarios",
        ["usuario_id"],
        ["id"]
    )


def downgrade():
    # Remove primeiro a chave estrangeira.
    op.drop_constraint(
        "fk_pacientes_usuario_id",
        "pacientes",
        type_="foreignkey"
    )

    # Depois remove a coluna.
    op.drop_column("pacientes", "usuario_id")
