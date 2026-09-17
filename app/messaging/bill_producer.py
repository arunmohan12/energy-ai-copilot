import json
import aio_pika
from app.messaging.rabbitmq import connect_rabbitmq

EXCHANGE_NAME = "energy_ai"

QUEUE_NAME = "bill_processing"
RETRY_QUEUE_NAME = "bill_retry"
FAILED_QUEUE_NAME = "bill_failed"

ROUTING_KEY = "bill.process"
RETRY_ROUTING_KEY = "bill.retry"
FAILED_ROUTING_KEY = "bill.failed"


async def publish_bill_processing_job(bill_id: int):
    connection,channel = await connect_rabbitmq()

    exchange = await channel.declare_exchange(EXCHANGE_NAME,aio_pika.ExchangeType.DIRECT,durable=True)  #check if exchange is availabl
    queue = await channel.declare_queue(QUEUE_NAME,durable=True)
    await queue.bind(exchange,ROUTING_KEY)

    retry_queue = await channel.declare_queue(RETRY_QUEUE_NAME,durable=True,
                                              arguments={
                                                  "x-message-ttl": 10000,
                                                  "x-dead-letter-exchange": EXCHANGE_NAME,
                                                  "x-dead-letter-routing-key": ROUTING_KEY,
                                              },
                                              )
    await retry_queue.bind(
        exchange,
        routing_key=RETRY_ROUTING_KEY,
    )
    failed_queue = await channel.declare_queue(
        FAILED_QUEUE_NAME,
        durable=True,
    )
    await failed_queue.bind(
        exchange,
        routing_key=FAILED_ROUTING_KEY,
    )
    message = {
        "bill_id":bill_id,
        "retry_count":0,
    }

    await exchange.publish(
        aio_pika.Message(
            body=json.dumps(message).encode(),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        ),
        routing_key=ROUTING_KEY,
    )

    await connection.close()




async def publish_bill_retry_job(bill_id: int):
    connection, channel = await connect_rabbitmq()

    exchange = await channel.declare_exchange(
        EXCHANGE_NAME,
        aio_pika.ExchangeType.DIRECT,
        durable=True,
    )

    queue = await channel.declare_queue(
        QUEUE_NAME,
        durable=True,
    )

    await queue.bind(
        exchange,
        routing_key=ROUTING_KEY,
    )

    message = {
        "bill_id": bill_id,
        "retry_count": 0,
    }

    await exchange.publish(
        aio_pika.Message(
            body=json.dumps(message).encode(),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        ),
        routing_key=ROUTING_KEY,
    )

    await connection.close()