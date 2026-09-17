import asyncio
import json

import aio_pika

from app.database import SessionLocal
from app.messaging.rabbitmq import connect_rabbitmq
from app.messaging.retry import MAX_RETRIES
from app.models.energy_bill import EnergyBill
from app.services.bill_processing import process_bill_extraction

EXCHANGE_NAME = "energy_ai"
RETRY_ROUTING_KEY = "bill.retry"
FAILED_ROUTING_KEY = "bill.failed"
QUEUE_NAME = "bill_processing"


async def process_message(message, exchange):
    async with message.process():
        data = json.loads(message.body)

        bill_id = data["bill_id"]
        retry_count = data.get("retry_count", 0)

        db = SessionLocal()
        bill = None

        try:
            bill = db.get(EnergyBill, bill_id)

            if bill is None:
                print(f"Bill {bill_id} not found")
                return
            if bill.status == "validated":
                print(
                    f"Bill {bill_id} is already validated. "
                    f"Skipping duplicate processing."
                )
                return

            bill.status = "processing"
            db.commit()

            print(
                f"Processing bill {bill_id} "
                f"(attempt {retry_count + 1})..."
            )

            processed_bill = process_bill_extraction(
                db,
                bill,
            )

            print(
                f"Bill {bill_id} processed "
                f"with status: {processed_bill.status}"
            )

        except Exception as exc:
            print(
                f"Bill {bill_id} failed: {exc}"
            )

            if retry_count < MAX_RETRIES:
                next_retry_count = retry_count + 1

                retry_message = {
                    "bill_id": bill_id,
                    "retry_count": next_retry_count,
                }

                await exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(
                            retry_message
                        ).encode(),
                        content_type="application/json",
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    ),
                    routing_key=RETRY_ROUTING_KEY,
                )

                print(
                    f"Bill {bill_id} scheduled for "
                    f"retry {next_retry_count}/{MAX_RETRIES}"
                )

            else:
                if bill is not None:
                    bill.status = "failed"
                    db.commit()

                failed_message = {
                    "bill_id": bill_id,
                    "retry_count": retry_count,
                    "error": str(exc),
                }

                await exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(
                            failed_message
                        ).encode(),
                        content_type="application/json",
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    ),
                    routing_key=FAILED_ROUTING_KEY,
                )

                print(
                    f"Bill {bill_id} exceeded maximum retries "
                    f"and was moved to bill_failed"
                )

        finally:
            db.close()


async def start_worker():
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
        routing_key="bill.process",
    )

    await queue.consume(
        lambda message: process_message(
            message,
            exchange,
        )
    )

    print(
        f"Worker listening on queue: {QUEUE_NAME}"
    )

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start_worker())