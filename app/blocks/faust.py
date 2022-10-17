import faust
from config import settings
from logger import logger
from models import Block
from db.utils import session_decorator
from utils import from_timestamp


class App(faust.App):
    pass


app = App("block", broker=settings.kafka_url)
blocks_topic = app.topic(
    "block",
    acks=True,
)


@session_decorator(add_param=False)
async def add_block(block_data: dict):
    await Block.get_or_create(
        hash=block_data["blockHash"],
        defaults={
            "number": block_data["blockNumber"],
            "timestamp": from_timestamp(block_data["timeStamp"]),
            "transaction_ids": block_data["transactionList"],
        }
    )


@app.agent(blocks_topic)
async def on_new_blocks(blocks_stream):
    async for block in blocks_stream:
        print(f"Get new block {block}")
        await add_block(block)
