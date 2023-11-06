import typing

from fastapi import HTTPException, status, Path

from .config import settings


async def validate_switch_name(switch_name: typing.Annotated[str, Path()]) -> str:
    if switch_name not in settings.switches:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid switch name")

    return switch_name
