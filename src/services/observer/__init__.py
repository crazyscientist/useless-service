import asyncio
import datetime
import random
import uuid

from aio_pika.abc import AbstractMessage

from ...libs.amqp import publish, RoutingKey
from ...libs.models import AuditModel, AuditAction, SwitchState
from .config import settings


async def on_change(message: AbstractMessage):
    data = AuditModel.model_validate_json(message.body)
    if data.switch.state is SwitchState.OFF:
        return

    await asyncio.sleep(1 + random.random() * 3)
    key = RoutingKey(switch=data.switch.name, action="request")
    await publish(settings=settings.amqp,
                  routing_key=key,
                  message=AuditModel(
                      timestamp=datetime.datetime.now(tz=datetime.UTC),
                      action=AuditAction.REQUEST,
                      switch=data.switch,
                      details="Switch was toggled on. Requesting to change state.",
                      transaction_id=uuid.uuid4()
                  ))
