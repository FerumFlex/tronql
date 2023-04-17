import sqlalchemy as sa
from db.base import Base


class Network(Base):
    __tablename__ = "networks"

    slug = sa.Column(sa.String(40), nullable=False, primary_key=True)
    title = sa.Column(sa.String(100), nullable=False)
    domain = sa.Column(sa.String(100), nullable=False)

    header_in_domain = sa.Column(sa.Boolean, default=False, nullable=False)
