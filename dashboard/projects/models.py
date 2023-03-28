import sqlalchemy as sa
from db.base import Base


class Plan(Base):
    __tablename__ = "projects_plans"

    id = sa.Column(sa.Integer, nullable=False, primary_key=True, autoincrement=True)
    slug = sa.Column(sa.String(20), nullable=False, unique=True)

    requests_per_month = sa.Column(sa.Integer, nullable=False)
    rate_limit = sa.Column(sa.Integer, nullable=False)
    rate_period = sa.Column(sa.Integer, nullable=False)

    title = sa.Column(sa.Text, nullable=True)
    description = sa.Column(sa.Text, nullable=True)

    visibility = sa.Column(sa.String(20), nullable=False)
    price = sa.Column(sa.Numeric(precision=60, scale=18), nullable=True)
    currency = sa.Column(sa.String(20), nullable=True)


class Project(Base):
    __tablename__ = "projects"

    id = sa.Column(sa.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(100), nullable=False)
    token = sa.Column(sa.String(100), nullable=False, unique=True)

    user_id = sa.Column(sa.String(100), nullable=False)

    plan_id = sa.Column(sa.Integer, sa.ForeignKey(Plan.id), nullable=False)
