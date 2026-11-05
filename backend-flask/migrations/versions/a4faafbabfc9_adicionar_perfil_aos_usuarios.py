
"""Adicionar perfil aos usuários."""

from alembic import op
import sqlalchemy as sa

revision = "a4faafbabfc9"
down_revision = "4307ce7c446a"
branch_labels = None
depends_on = None


def upgrade():
    # Adiciona o perfil dos usuários.
    op.add_column(
        "usuarios",
        sa.Column(
            "perfil",
            sa.String(20),
            nullable=False,
            server_default="profissional"
        )
    )


def downgrade():
    # Remove a coluna caso a migração seja revertida.
    op.drop_column("usuarios", "perfil")
