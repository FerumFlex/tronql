"""add_network_field

Revision ID: c8995f3d5ef3
Revises: f3426fc5ced0
Create Date: 2023-04-14 19:09:44.636900

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c8995f3d5ef3"
down_revision = "f3426fc5ced0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "projects", sa.Column("network_slug", sa.String(length=40), nullable=True)
    )
    op.execute("UPDATE projects SET network_slug='tron-mainnet';")
    op.alter_column("projects", "network_slug", nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("projects", "network_slug")
    # ### end Alembic commands ###
