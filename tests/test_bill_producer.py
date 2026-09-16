import pytest

from app.messaging.bill_producer import publish_bill_processing_job

@pytest.mark.asyncio
async def test_publish_bill_processing_job():
    await publish_bill_processing_job(2)