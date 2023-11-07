import datetime
import enum
import typing

from pydantic import BaseModel
from pydantic.types import UUID4


class SwitchState(enum.StrEnum):
    ON = "on"
    OFF = "off"


class SwitchModel(BaseModel):
    name: str
    state: SwitchState


class AuditAction(enum.StrEnum):
    CHANGED = "changed"
    REQUEST = "request"
    APPROVED = "approved"


class AuditModel(BaseModel):
    timestamp: datetime.datetime
    action: AuditAction
    switch: typing.Optional[SwitchModel] = None
    details: typing.Optional[str] = None
    transaction_id: typing.Optional[UUID4] = None
