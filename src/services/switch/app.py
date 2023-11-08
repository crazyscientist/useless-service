import asyncio
import datetime
import typing
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Depends, status, Body, WebSocket, WebSocketDisconnect
from redis.asyncio.client import Redis
from redis.asyncio.lock import Lock

from ...libs.amqp import publish, subscribe, RoutingKey
from ...libs.cache import get_redis
from ...libs.models import SwitchState, SwitchModel, AuditAction, AuditModel, AuditTransaction

from .config import settings
from .utils import validate_switch_name


app = FastAPI(title="Useless Machine API",
              summary="Machine to toggle a switch off",
              description="This API provides the interface for external users to interact with "
                          "the switches of the useless machine",
              version="१.६.९९")


@app.get("/")
async def list_switches() -> list[str]:
    return settings.switches


@app.get("/{switch_name}",
         dependencies=[Depends(validate_switch_name)],
         responses={404: {"description": "Invalid switch name"}})
async def get_switch_state(switch_name: str, redis: Redis = Depends(get_redis)) -> SwitchModel:
    state = await redis.get(switch_name)
    return SwitchModel(name=switch_name, state=state or SwitchState.OFF)


@app.websocket("/{switch_name}",
               dependencies=[Depends(validate_switch_name)])
async def get_switch_log(switch_name: str, websocket: WebSocket):
    await websocket.accept()
    try:
        routing_key = RoutingKey(switch=switch_name, action="*")
        queue = await subscribe(settings=settings.amqp, routing_key=routing_key)
        consumer_tag = uuid4().hex

        async def _private_callback(message):
            try:
                await websocket.send_text(message.body)
            except RuntimeError:
                await queue.cancel(consumer_tag=consumer_tag)

        await queue.consume(callback=_private_callback, consumer_tag=consumer_tag)
        while True:
            msg = await websocket.receive()
            if msg.get("type", None) == 'websocket.disconnect':
                break
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass


@app.put("/{switch_name}",
         dependencies=[Depends(validate_switch_name)],
         responses={404: {"description": "Invalid switch name"}})
async def set_switch_state(switch_name: str,
                           state: typing.Annotated[SwitchState, Body()],
                           redis: Redis = Depends(get_redis))\
        -> SwitchModel:
    lock = Lock(redis=redis, name=f"LOCK:{switch_name}", timeout=2)

    async with lock:
        old_state = await redis.get(switch_name)
        if old_state:
            old_state = SwitchState[old_state.decode().upper()]
        if old_state is state:

            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                                detail=f"State is already set to '{state}'")

        await redis.set(switch_name, state)

    switch = SwitchModel(name=switch_name, state=state)

    await publish(settings=settings.amqp,
                  routing_key=RoutingKey(switch=switch_name, action=AuditAction.CHANGED),
                  message=AuditModel(
                      timestamp=datetime.datetime.now(tz=datetime.UTC),
                      action=AuditAction.CHANGED,
                      switch=switch,
                      details="Switch was toggled"
                  ))
    return switch


@app.get("/{switch_name}/audit-log",
         dependencies=[Depends(validate_switch_name)])
async def get_switch_auditlog(switch_name: str,
                              redis: Redis = Depends(get_redis)) -> list[AuditTransaction]:
    transactions = await redis.smembers(name=f"auditlog.{switch_name}")

    if transactions:
        transactions = [AuditTransaction.model_validate_json(t) for t in transactions]
    else:
        transactions = []

    return transactions
