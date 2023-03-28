import pathlib
import sys

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

BASE_DIR = pathlib.Path(__file__).parent
sys.path.append(str(BASE_DIR.parent))

from db.base import Base


class Block(Base):
    __tablename__ = "blocks"

    hash = sa.Column(sa.String(100), primary_key=True, nullable=False)
    number = sa.Column(sa.Integer, unique=True, nullable=False)
    timestamp = sa.Column(sa.TIMESTAMP, nullable=False)
    transaction_ids = sa.Column(sa.ARRAY(sa.String), nullable=False)


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = sa.Column(sa.String(100), primary_key=True, nullable=False)
    block_hash = sa.Column(sa.String(100), primary_key=True, nullable=False)
    time_stamp = sa.Column(sa.TIMESTAMP, nullable=False)
    block_number = sa.Column(sa.BigInteger, nullable=False)
    energy_usage = sa.Column(sa.Integer, nullable=False)
    energy_fee = sa.Column(sa.Integer, nullable=False)
    origin_energy_usage = sa.Column(sa.Integer, nullable=False)
    energy_usage_total = sa.Column(sa.Integer, nullable=False)
    net_usage = sa.Column(sa.Integer, nullable=False)
    net_fee = sa.Column(sa.Integer, nullable=False)
    result = sa.Column(sa.String, nullable=True)
    trigger_name = sa.Column(sa.String, nullable=True)
    contract_address = sa.Column(sa.String, nullable=True)
    contract_type = sa.Column(sa.String, nullable=True)
    fee_limit = sa.Column(sa.Integer, nullable=False)
    contract_call_value = sa.Column(sa.Integer, nullable=False)
    contract_result = sa.Column(sa.String, nullable=True)
    from_address = sa.Column(sa.String, nullable=True)
    to_address = sa.Column(sa.String, nullable=True)
    asset_name = sa.Column(sa.String, nullable=True)
    asset_amount = sa.Column(sa.BigInteger, nullable=True)
    internal_transaction_list = sa.Column(JSONB, nullable=True)
    data = sa.Column(sa.String, nullable=True)
    transaction_index = sa.Column(sa.Integer, nullable=False)
    cumulative_energy_used = sa.Column(sa.Integer, nullable=False)
    pre_cumulative_log_count = sa.Column(sa.Integer, nullable=False)
    log_list = sa.Column(JSONB, nullable=True)
    energy_unit_price = sa.Column(sa.Integer, nullable=False)
