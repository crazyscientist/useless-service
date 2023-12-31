import datetime
from unittest import IsolatedAsyncioTestCase, mock
from uuid import uuid4

from aio_pika import Message

from ...libs.cache import get_redis
from ...libs.models import AuditAction, AuditModel, AuditTransaction, SwitchState, SwitchModel
from . import on_action, get_transaction, LOG_TEMPLATE


async def ack(*args, **kwargs):
    ...


class AuditorTest(IsolatedAsyncioTestCase):
    switch = SwitchModel(name="switch-1", state=SwitchState.ON)
    transaction_id = uuid4()

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.redis = await get_redis()
        await self.redis.flushall()

    def create_message(self, action: AuditAction) -> Message:
        msg = Message(
            body=AuditModel(
                timestamp=datetime.datetime.now(tz=datetime.UTC),
                action=action,
                switch=self.switch,
                transaction_id=self.transaction_id
            ).model_dump_json().encode(),
            content_type="text/json"
        )
        msg.ack = ack
        return msg

    async def test_request(self):
        await on_action(self.create_message(AuditAction.REQUEST))
        transaction = await get_transaction(redis=self.redis, transaction_id=self.transaction_id,
                                            timestamp=datetime.datetime.now(tz=datetime.UTC),
                                            switch=self.switch.name)
        self.assertEqual(len(transaction.details), 1)
        self.assertEqual(transaction.details[0].action, AuditAction.REQUEST)

        auditlog = await self.redis.smembers(LOG_TEMPLATE.format(self.switch.name))
        self.assertEqual(len(auditlog), 0)

    async def test_approved(self):
        await on_action(self.create_message(AuditAction.REQUEST))
        await on_action(self.create_message(AuditAction.APPROVED))
        transaction = await get_transaction(redis=self.redis, transaction_id=self.transaction_id,
                                            timestamp=datetime.datetime.now(tz=datetime.UTC),
                                            switch=self.switch.name)
        self.assertEqual(len(transaction.details), 2)
        self.assertEqual(transaction.details[0].action, AuditAction.REQUEST)

        auditlog = await self.redis.smembers(LOG_TEMPLATE.format(self.switch.name))
        self.assertEqual(len(auditlog), 0)

    async def test_denied(self):
        await on_action(self.create_message(AuditAction.REQUEST))
        await on_action(self.create_message(AuditAction.DENIED))

        with self.subTest("Cache"):
            transaction = await get_transaction(redis=self.redis, transaction_id=self.transaction_id,
                                                timestamp=datetime.datetime.now(tz=datetime.UTC),
                                                switch=self.switch.name)
            self.assertEqual(len(transaction.details), 0)

        with self.subTest("Auditlog"):
            auditlog = await self.redis.smembers(LOG_TEMPLATE.format(self.switch.name))
            self.assertEqual(len(auditlog), 1)
            auditlog = [AuditTransaction.model_validate_json(x) for x in auditlog]
            self.assertEqual(len(auditlog[0].details), 2)
            self.assertEqual(auditlog[0].details[0].action, AuditAction.REQUEST)

    async def test_executed(self):
        await on_action(self.create_message(AuditAction.REQUEST))
        await on_action(self.create_message(AuditAction.APPROVED))
        await on_action(self.create_message(AuditAction.EXECUTED))

        with self.subTest("Cache"):
            transaction = await get_transaction(redis=self.redis, transaction_id=self.transaction_id,
                                                timestamp=datetime.datetime.now(tz=datetime.UTC),
                                                switch=self.switch.name)
            # Transaction is finished and no longer cached
            self.assertEqual(len(transaction.details), 0)

        with self.subTest("Auditlog"):
            auditlog = await self.redis.smembers(LOG_TEMPLATE.format(self.switch.name))
            self.assertEqual(len(auditlog), 1)
            auditlog = [AuditTransaction.model_validate_json(x) for x in auditlog]
            self.assertEqual(len(auditlog[0].details), 3)
            self.assertEqual(auditlog[0].details[0].action, AuditAction.REQUEST)
