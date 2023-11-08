import asyncio
import datetime
import random
import uuid

from aio_pika import IncomingMessage

from ...libs.amqp import publish, RoutingKey
from ...libs.config import settings
from ...libs.models import AuditModel, AuditAction, SwitchState


async def on_change(message: IncomingMessage):
    data = AuditModel.model_validate_json(message.body)
    if data.switch.state is SwitchState.OFF:
        return

    await asyncio.sleep(1 + random.random() * 3)
    key = RoutingKey(switch=data.switch.name, action=AuditAction.REQUEST)
    await publish(settings=settings.amqp,
                  routing_key=key,
                  message=AuditModel(
                      timestamp=datetime.datetime.now(tz=datetime.UTC),
                      action=AuditAction.REQUEST,
                      switch=data.switch,
                      details="Switch was toggled on. Requesting to change state.",
                      transaction_id=uuid.uuid4()
                  ))
    await message.ack()
