import faust
from config import settings
from logger import logger
from models import Transaction
from db.utils import session_decorator
from utils import from_timestamp, camel_to_snake_dict


class App(faust.App):
    pass


app = App("transaction", broker=settings.kafka_url)
transactions_topic = app.topic(
    "transaction",
    acks=True,
)


@session_decorator(add_param=False)
async def add_transaction(trans_data: dict):
    data = camel_to_snake_dict(trans_data)
    transaction_id = data.pop("transaction_id")
    data["time_stamp"] = from_timestamp(data["time_stamp"])
    del data["latest_solidified_block_number"]
    await Transaction.get_or_create(
        transaction_id=transaction_id,
        defaults=data,
    )


@app.agent(transactions_topic)
async def on_new_transactions(transactions_stream):
    async for trans in transactions_stream:
        print(f"Get new trans {trans}")
        await add_transaction(trans)
