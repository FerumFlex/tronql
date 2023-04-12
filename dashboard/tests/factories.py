import asyncio

import factory
from db.base import Session
from projects.models import Project


class BaseFactory(factory.Factory):
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def create_coro(*args, **kwargs):
            params = {}
            for key, value in kwargs.items():
                if asyncio.iscoroutine(value):
                    obj = await value
                    params[key] = obj.id
                else:
                    params[key] = value

            async with Session(expire_on_commit=False) as session:
                async with session.begin():
                    model = model_class(*args, **params)
                    session.add(model)
                    return model

        return create_coro(*args, **kwargs)


class ProjectFactory(BaseFactory):
    class Meta:
        model = Project

    name = factory.Sequence(lambda n: f"project{n}")
    token = factory.Sequence(lambda n: f"token{n}")

    user_id = "123"
    plan_id = "basic"
