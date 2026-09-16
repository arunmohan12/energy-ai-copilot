import pytest
from app.messaging.rabbitmq import connect_rabbitmq

@pytest.mark.asyncio
async def test_rabbitmq_connection():
    connection, channel = await connect_rabbitmq()
    assert connection is not None
    assert channel is not None

    await connection.close()


