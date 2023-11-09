import datetime
from urllib.parse import urljoin

from aio_pika.abc import AbstractMessage

from ...libs import delay
from ...libs.amqp import publish, RoutingKey
from ...libs.config import settings
from ...libs.http import get_client
from ...libs.models import AuditAction, AuditModel, SwitchState, SwitchModel


async def on_approval(message: AbstractMessage):
    data = AuditModel.model_validate_json(message.body)
    await delay(scale=5)

    async with get_client() as client:
        response = await client.put(url=urljoin(str(settings.base_url),
                                                data.switch.name),
                                    json=SwitchState.OFF)
        switch = data.switch
        action = AuditAction.EXECUTED
        if response.status_code == 200:
            switch = SwitchModel.model_validate_json(response.text)
            details = "Switch turned off."
        else:
            details = response.json().get("detail", "Unknown error.")
            action = AuditAction.ABORTED
            if response.status_code == 208:
                switch.state = SwitchState.OFF
        await publish(settings=settings.amqp,
                      routing_key=RoutingKey(switch=data.switch.name, action=action),
                      message=AuditModel(
                          timestamp=datetime.datetime.now(tz=datetime.UTC),
                          action=action,
                          switch=switch,
                          details=f"Transaction completed: {details}",
                          transaction_id=data.transaction_id
                      ))
