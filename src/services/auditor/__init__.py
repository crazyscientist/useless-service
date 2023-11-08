import typing
from uuid import UUID

from aio_pika import IncomingMessage
from redis.asyncio import Redis

from ...libs.cache import get_redis
from ...libs.models import AuditModel, AuditTransaction, AuditAction, TransactionDetail


LOG_TEMPLATE = "auditlog.{}"
TRANSACTION_TEMPLATE = "transaction.{}"


async def get_transaction(redis: Redis, transaction_id: UUID, switch: typing.Optional[str] = None) \
        -> AuditTransaction:
    key = TRANSACTION_TEMPLATE.format(transaction_id)
    transaction = await redis.get(key)
    if transaction:
        return AuditTransaction.model_validate_json(transaction)

    return AuditTransaction(id=transaction_id, switch=switch, details=[])


async def on_action(message: IncomingMessage):
    data = AuditModel.model_validate_json(message.body)
    if data.transaction_id is None:
        await message.ack()
        return

    transaction_key = TRANSACTION_TEMPLATE.format(data.transaction_id)

    redis = await get_redis()
    transaction = await get_transaction(redis=redis, transaction_id=data.transaction_id,
                                        switch=data.switch.name)
    transaction.details.append(TransactionDetail(timestamp=data.timestamp, action=data.action))
    await redis.set(name=transaction_key, value=transaction.model_dump_json(), ex=3600)

    if data.action in [AuditAction.EXECUTED, AuditAction.DENIED]:
        await redis.sadd(LOG_TEMPLATE.format(data.switch.name), transaction.model_dump_json())

    await message.ack()
