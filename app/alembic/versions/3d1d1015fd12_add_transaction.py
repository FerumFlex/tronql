"""add_transaction

Revision ID: 3d1d1015fd12
Revises: 2988aa9bc036
Create Date: 2022-10-12 14:37:39.016811

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3d1d1015fd12"
down_revision = "2988aa9bc036"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "transactions",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=True,
        ),
        sa.Column("transaction_id", sa.String(length=100), nullable=False),
        sa.Column("block_hash", sa.String(length=100), nullable=False),
        sa.Column("time_stamp", sa.TIMESTAMP(), nullable=False),
        sa.Column("block_number", sa.BigInteger(), nullable=False),
        sa.Column("energy_usage", sa.Integer(), nullable=False),
        sa.Column("energy_fee", sa.Integer(), nullable=False),
        sa.Column("origin_energy_usage", sa.Integer(), nullable=False),
        sa.Column("energy_usage_total", sa.Integer(), nullable=False),
        sa.Column("net_usage", sa.Integer(), nullable=False),
        sa.Column("net_fee", sa.Integer(), nullable=False),
        sa.Column("result", sa.String(), nullable=True),
        sa.Column("trigger_name", sa.String(), nullable=True),
        sa.Column("contract_address", sa.String(), nullable=True),
        sa.Column("contract_type", sa.String(), nullable=True),
        sa.Column("fee_limit", sa.Integer(), nullable=False),
        sa.Column("contract_call_value", sa.Integer(), nullable=False),
        sa.Column("contract_result", sa.String(), nullable=True),
        sa.Column("from_address", sa.String(), nullable=True),
        sa.Column("to_address", sa.String(), nullable=True),
        sa.Column("asset_name", sa.String(), nullable=True),
        sa.Column("asset_amount", sa.BigInteger(), nullable=True),
        sa.Column(
            "internal_transaction_list",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("data", sa.String(), nullable=True),
        sa.Column("transaction_index", sa.Integer(), nullable=False),
        sa.Column("cumulative_energy_used", sa.Integer(), nullable=False),
        sa.Column("pre_cumulative_log_count", sa.Integer(), nullable=False),
        sa.Column("log_list", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("energy_unit_price", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("transaction_id", "block_hash"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transactions")
    # ### end Alembic commands ###
