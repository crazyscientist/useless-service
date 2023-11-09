import datetime
from unittest import IsolatedAsyncioTestCase, mock

from aio_pika import Message
import httpx

from ...libs.models import SwitchState, SwitchModel, AuditModel, AuditAction
from . import on_approval


class WorkerTest(IsolatedAsyncioTestCase):
    @staticmethod
    def get_mocked_client(http_status=200, switch_state=SwitchState.OFF, detail=None):
        def handler(request):
            return httpx.Response(http_status,
                                  text=SwitchModel(name="switch-1", state=switch_state).model_dump_json())

        def detail_handler(request):
            return httpx.Response(http_status, json={"detail": detail})

        if detail:
            transport = httpx.MockTransport(handler=detail_handler)
        else:
            transport = httpx.MockTransport(handler=handler)

        return httpx.AsyncClient(transport=transport)

    async def test_switch_off(self):
        with mock.patch("src.services.worker.publish") as mocked_publish, \
                mock.patch("src.services.worker.get_client",
                           return_value=self.get_mocked_client()) as mocked_client:
            await on_approval(message=Message(
                body=AuditModel(
                    timestamp=datetime.datetime.now(tz=datetime.UTC),
                    action=AuditAction.APPROVED,
                    switch=SwitchModel(name="switch-1", state=SwitchState.ON)
                ).model_dump_json().encode(),
                content_type="text/json"
            ))
            self.assertEqual(mocked_publish.call_count, 1)
            published = mocked_publish.call_args_list[0].kwargs["message"]
            self.assertEqual(published.action, AuditAction.EXECUTED)
            self.assertEqual(published.switch.state, SwitchState.OFF)

    async def test_switch_already_off(self):
        with mock.patch("src.services.worker.publish") as mocked_publish, \
                mock.patch("src.services.worker.get_client",
                           return_value=self.get_mocked_client(208, SwitchState.OFF, "already set to off")) as mocked_client:
            await on_approval(message=Message(
                body=AuditModel(
                    timestamp=datetime.datetime.now(tz=datetime.UTC),
                    action=AuditAction.APPROVED,
                    switch=SwitchModel(name="switch-1", state=SwitchState.ON)
                ).model_dump_json().encode(),
                content_type="text/json"
            ))
            self.assertEqual(mocked_publish.call_count, 1)
            published = mocked_publish.call_args_list[0].kwargs["message"]
            self.assertEqual(published.action, AuditAction.ABORTED)
            self.assertEqual(published.switch.state, SwitchState.OFF)
            self.assertIn("already set to", published.details)

    async def test_http_error(self):
        with mock.patch("src.services.worker.publish") as mocked_publish, \
                mock.patch("src.services.worker.get_client",
                           return_value=self.get_mocked_client(500, SwitchState.OFF, "foo bar")) as mocked_client:
            await on_approval(message=Message(
                body=AuditModel(
                    timestamp=datetime.datetime.now(tz=datetime.UTC),
                    action=AuditAction.APPROVED,
                    switch=SwitchModel(name="switch-1", state=SwitchState.ON)
                ).model_dump_json().encode(),
                content_type="text/json"
            ))
            self.assertEqual(mocked_publish.call_count, 1)
            published = mocked_publish.call_args_list[0].kwargs["message"]
            self.assertEqual(published.action, AuditAction.ABORTED)
            self.assertEqual(published.switch.state, SwitchState.ON)
            self.assertIn("foo bar", published.details)
