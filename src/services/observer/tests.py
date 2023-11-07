import datetime
from unittest import IsolatedAsyncioTestCase, mock

from aio_pika import Message

from ...libs.models import AuditModel, AuditAction, SwitchModel, SwitchState
from . import on_change


class ObserverTest(IsolatedAsyncioTestCase):
    def create_message(self, state: SwitchState) -> Message:
        return Message(
            body=AuditModel(
                timestamp=datetime.datetime.now(tz=datetime.UTC),
                action=AuditAction.CHANGED,
                switch=SwitchModel(name="switch-1", state=state)
            ).model_dump_json().encode(),
            content_type="text/json"
        )

    async def test_switch_on(self):
        with mock.patch("src.services.observer.publish") as mocked_publish:
            await on_change(message=self.create_message(state=SwitchState.ON))
            self.assertEqual(mocked_publish.call_count, 1)
            published_msg = mocked_publish.call_args_list[0].kwargs.get("message")
            self.assertIsInstance(published_msg, AuditModel)
            self.assertEqual(published_msg.action, AuditAction.REQUEST)

    async def test_switch_off(self):
        with mock.patch("src.services.observer.publish") as mocked_publish:
            await on_change(message=self.create_message(state=SwitchState.OFF))
            self.assertEqual(mocked_publish.call_count, 0)
