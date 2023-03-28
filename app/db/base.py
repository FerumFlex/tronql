import contextvars
import datetime
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

import sqlalchemy as sa
from config import settings
from db.proxy import SessionProxy
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Model = declarative_base()
session_context = contextvars.ContextVar("session")
current_session = SessionProxy(session_context)
Session = sessionmaker(class_=AsyncSession)


class Base(Model):
    __abstract__ = True

    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.text("NOW()"))
    updated_at = sa.Column(
        sa.DateTime(timezone=True),
        server_default=sa.text("NOW()"),
        onupdate=datetime.datetime.utcnow,
    )

    def to_dict(self, exclude: List[str] = []) -> Dict[str, Any]:
        return {
            c.key: getattr(self, c.key)
            for c in sa.inspect(self).mapper.column_attrs
            if c.key not in exclude
        }

    @classmethod
    async def get_or_create(
        cls, defaults: Optional[dict] = None, **kwargs
    ) -> Tuple[Model, bool]:
        if obj := await cls.get(**kwargs):
            return obj, False

        defaults = defaults or {}
        return await cls.create(**kwargs, **defaults), True

    @classmethod
    async def get(cls, iter_pks: Union[Any, Iterator[Any]] = None, **kwargs):
        if iter_pks is not None:
            if not isinstance(iter_pks, (tuple, list)):
                iter_pks = (iter_pks,)

            where = {
                pk.name: cond for pk, cond in zip(cls.__table__.primary_key, iter_pks)
            }
            kwargs.update(where)

        query = sa.select(cls).filter_by(**kwargs)
        result = await current_session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def create(cls, **kwargs) -> Model:
        obj = cls(**kwargs)

        current_session.add(obj)
        await current_session.flush()
        await current_session.refresh(obj)

        return obj

    async def update(self, **kwargs) -> Model:
        for key, value in kwargs.items():
            setattr(self, key, value)
        await current_session.flush()
        await current_session.refresh(self)
        return self

    async def delete(self) -> bool:
        await current_session.delete(self)
        return True

    @classmethod
    async def exists(cls, iter_pks: Union[tuple, list] = None, **kwargs) -> bool:
        if iter_pks is not None:
            if not isinstance(iter_pks, (tuple, list)):
                iter_pks = [iter_pks]
            where = {
                pk.name: cond for pk, cond in zip(cls.__table__.primary_key, iter_pks)
            }
            kwargs.update(where)

        query = sa.select([1]).select_from(cls).filter_by(**kwargs).exists().select()
        return bool((await current_session.execute(query)).scalars().one())


async def init_db():
    engine = create_async_engine(settings.database_url, pool_recycle=600)
    Session.configure(bind=engine)
    return engine


engine = create_async_engine(settings.database_url, pool_recycle=600)
Session.configure(bind=engine)
