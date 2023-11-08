import datetime
from urllib.parse import urljoin

from aio_pika import IncomingMessage

from ...libs.amqp import publish, RoutingKey
from ...libs.config import settings
from ...libs.http import get_client
from ...libs.models import AuditModel, AuditAction, SwitchState, SwitchModel


async def on_request(message: IncomingMessage):
    data = AuditModel.model_validate_json(message.body)
    if data.switch.state is SwitchState.OFF:
        await publish(settings=settings.amqp,
                      routing_key=RoutingKey(switch=data.switch.name,
                                             action=AuditAction.DENIED),
                      message=AuditModel(
                          timestamp=datetime.datetime.now(tz=datetime.UTC),
                          action=AuditAction.DENIED,
                          switch=data.switch,
                          details="Request denied: According to request switch is already off.",
                          transaction_id=data.transaction_id
                      ))
        await message.ack()
        return

    async with get_client() as client:
        response = await client.get(url=urljoin(str(settings.base_url),
                                                data.switch.name))
        if response.status_code >= 400:
            await publish(settings=settings.amqp,
                          routing_key=RoutingKey(switch=data.switch.name,
                                                 action=AuditAction.DENIED),
                          message=AuditModel(
                              timestamp=datetime.datetime.now(tz=datetime.UTC),
                              action=AuditAction.DENIED,
                              switch=data.switch,
                              details="Request denied: Failed to obtain current state of switch.",
                              transaction_id=data.transaction_id
                          ))
            await message.ack()
            return

        switch = SwitchModel.model_validate_json(response.text)
        if switch.state is SwitchState.OFF:
            await publish(settings=settings.amqp,
                          routing_key=RoutingKey(switch=data.switch.name,
                                                 action=AuditAction.DENIED),
                          message=AuditModel(
                              timestamp=datetime.datetime.now(tz=datetime.UTC),
                              action=AuditAction.DENIED,
                              switch=data.switch,
                              details="Request denied: Actually switch is already off.",
                              transaction_id=data.transaction_id
                          ))
            await message.ack()
            return

    await publish(settings=settings.amqp,
                  routing_key=RoutingKey(switch=data.switch.name, action=AuditAction.APPROVED),
                  message=AuditModel(
                      timestamp=datetime.datetime.now(tz=datetime.UTC),
                      action=AuditAction.APPROVED,
                      switch=data.switch,
                      details="Request approved: Turn the switch off again!",
                      transaction_id=data.transaction_id
                  ))
    await message.ack()
    return
