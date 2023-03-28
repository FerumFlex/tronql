import sqlalchemy as sa
from db.base import Base


class ProjectStat(Base):
    __tablename__ = "stats_project"

    project_id = sa.Column(sa.Integer, nullable=False)
    date = sa.Column(sa.DateTime(timezone=True), nullable=False)
    user_id = sa.Column(sa.String(50), nullable=False)

    count = sa.Column(sa.Integer, nullable=False)

    __table_args__ = (
        sa.PrimaryKeyConstraint(project_id, date, name="project_stats_unique"),
        {},
    )
