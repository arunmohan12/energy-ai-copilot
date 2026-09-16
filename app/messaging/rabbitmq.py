import aio_pika


RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"


async def connect_rabbitmq():
    connection = await aio_pika.connect_robust(
        RABBITMQ_URL
    )

    channel = await connection.channel()

    return connection, channel