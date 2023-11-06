import datetime
from unittest import IsolatedAsyncioTestCase

from fastapi.testclient import TestClient

from ...libs.amqp import publish, RoutingKey
from ...libs.models import SwitchModel, SwitchState, AuditModel, AuditAction
from .app import app
from .cache import get_redis
from .config import settings


class SwitchTest(IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = TestClient(app=app)

    @classmethod
    def tearDownClass(cls):
        del cls.client
        super().tearDownClass()

    async def asyncSetUp(self):
        redis = await get_redis()
        await redis.flushdb()

    async def test_get_initial_switch_state(self):
        response = self.client.get("/switch-1")
        model = SwitchModel.model_validate_json(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(model, SwitchModel(name="switch-1", state=SwitchState.OFF))

    async def test_switch_state(self):
        response = self.client.put("/switch-1", json=SwitchState.ON)

        self.assertEqual(response.status_code, 200)

        response = self.client.get("/switch-1")
        model = SwitchModel.model_validate_json(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(model, SwitchModel(name="switch-1", state=SwitchState.ON))

    async def test_get_switch_log(self):
        with self.client.websocket_connect("/switch-1") as ws:
            await publish(settings=settings.amqp,
                          routing_key=RoutingKey(switch="switch-1", action="*"),
                          message=AuditModel(
                              timestamp=datetime.datetime.now(tz=datetime.UTC),
                              action=AuditAction.CHANGED,
                              switch=SwitchModel(
                                  name="switch-1",
                                  state=SwitchState.ON
                              )
                          ))
            ws_message = ws.receive_text()
        model = AuditModel.model_validate_json(ws_message)
        self.assertEqual(model.action, AuditAction.CHANGED)
        self.assertEqual(model.switch.state, SwitchState.ON)
