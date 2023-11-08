import datetime
from unittest import IsolatedAsyncioTestCase, mock

from aio_pika import Message
import httpx

from ...libs.models import SwitchState, SwitchModel, AuditModel, AuditAction
from . import on_request


async def ack(*args, **kwargs):
    ...


class ManagerTest(IsolatedAsyncioTestCase):
    @staticmethod
    def get_mocked_client(http_status=200, switch_state=SwitchState.OFF):
        def handler(request):
            return httpx.Response(http_status,
                                  text=SwitchModel(name="switch-1", state=switch_state).model_dump_json())

        return httpx.AsyncClient(transport=httpx.MockTransport(handler=handler))

    @staticmethod
    def create_message(state: SwitchState) -> Message:
        msg = Message(
                body=AuditModel(
                    timestamp=datetime.datetime.now(tz=datetime.UTC),
                    action=AuditAction.REQUEST,
                    switch=SwitchModel(name="switch-1", state=state)
                ).model_dump_json().encode(),
                content_type="text/json"
            )
        msg.ack = ack
        return msg

    async def test_switch_off_in_event(self):
        with mock.patch("src.services.manager.publish") as mocked_publish, \
                mock.patch("src.services.manager.get_client",
                           return_value=self.get_mocked_client()) as mocked_client:
            await on_request(message=self.create_message(SwitchState.OFF))
            self.assertEqual(mocked_publish.call_count, 1)
            published = mocked_publish.call_args_list[0].kwargs["message"]
            self.assertEqual(published.action, AuditAction.DENIED)

    async def test_switch_off_in_api(self):
        with mock.patch("src.services.manager.publish") as mocked_publish, \
                mock.patch("src.services.manager.get_client",
                           return_value=self.get_mocked_client()) as mocked_client:
            await on_request(message=self.create_message(SwitchState.ON))
            self.assertEqual(mocked_publish.call_count, 1)
            published = mocked_publish.call_args_list[0].kwargs["message"]
            self.assertEqual(published.action, AuditAction.DENIED)

    async def test_switch_on(self):
        with mock.patch("src.services.manager.publish") as mocked_publish, \
                mock.patch("src.services.manager.get_client",
                           return_value=self.get_mocked_client(switch_state=SwitchState.ON)) as mocked_client:
            await on_request(message=self.create_message(SwitchState.ON))
            self.assertEqual(mocked_publish.call_count, 1)
            published = mocked_publish.call_args_list[0].kwargs["message"]
            self.assertEqual(published.action, AuditAction.APPROVED)

    async def test_http_failure(self):
        with mock.patch("src.services.manager.publish") as mocked_publish, \
                mock.patch("src.services.manager.get_client",
                           return_value=self.get_mocked_client(http_status=404, switch_state=SwitchState.ON)) as mocked_client:
            await on_request(message=self.create_message(SwitchState.ON))
            self.assertEqual(mocked_publish.call_count, 1)
            published = mocked_publish.call_args_list[0].kwargs["message"]
            self.assertEqual(published.action, AuditAction.DENIED)
