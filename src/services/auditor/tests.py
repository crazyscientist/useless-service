import datetime
from unittest import IsolatedAsyncioTestCase, mock
from uuid import uuid4

from aio_pika import Message

from ...libs.cache import get_redis
from ...libs.models import AuditAction, AuditModel, SwitchState, SwitchModel
from . import on_action, get_transaction, LOG_TEMPLATE


class AuditorTest(IsolatedAsyncioTestCase):
    switch = SwitchModel(name="switch-1", state=SwitchState.ON)
    transaction_id = uuid4()

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.redis = await get_redis()
        await self.redis.flushall()

    def create_message(self, action: AuditAction) -> Message:
        return Message(
            body=AuditModel(
                timestamp=datetime.datetime.now(tz=datetime.UTC),
                action=action,
                switch=self.switch,
                transaction_id=self.transaction_id
            ).model_dump_json().encode(),
            content_type="text/json"
        )

    async def test_request(self):
        await on_action(self.create_message(AuditAction.REQUEST))
        transaction = await get_transaction(redis=self.redis, transaction_id=self.transaction_id)
        self.assertEqual(len(transaction.details), 1)
        self.assertEqual(transaction.details[0].action, AuditAction.REQUEST)

        auditlog = await self.redis.smembers(LOG_TEMPLATE.format(self.switch.name))
        self.assertEqual(len(auditlog), 0)

    async def test_approved(self):
        await on_action(self.create_message(AuditAction.REQUEST))
        await on_action(self.create_message(AuditAction.APPROVED))
        transaction = await get_transaction(redis=self.redis, transaction_id=self.transaction_id)
        self.assertEqual(len(transaction.details), 2)
        self.assertEqual(transaction.details[0].action, AuditAction.REQUEST)

        auditlog = await self.redis.smembers(LOG_TEMPLATE.format(self.switch.name))
        self.assertEqual(len(auditlog), 0)

    async def test_denied(self):
        await on_action(self.create_message(AuditAction.REQUEST))
        await on_action(self.create_message(AuditAction.DENIED))
        transaction = await get_transaction(redis=self.redis, transaction_id=self.transaction_id)
        self.assertEqual(len(transaction.details), 2)
        self.assertEqual(transaction.details[0].action, AuditAction.REQUEST)

        auditlog = await self.redis.smembers(LOG_TEMPLATE.format(self.switch.name))
        self.assertEqual(len(auditlog), 1)

    async def test_executed(self):
        await on_action(self.create_message(AuditAction.REQUEST))
        await on_action(self.create_message(AuditAction.APPROVED))
        await on_action(self.create_message(AuditAction.EXECUTED))
        transaction = await get_transaction(redis=self.redis, transaction_id=self.transaction_id)
        self.assertEqual(len(transaction.details), 3)
        self.assertEqual(transaction.details[0].action, AuditAction.REQUEST)

        auditlog = await self.redis.smembers(LOG_TEMPLATE.format(self.switch.name))
        self.assertEqual(len(auditlog), 1)
