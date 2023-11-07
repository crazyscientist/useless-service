from httpx import AsyncClient


def get_client() -> AsyncClient:
    return AsyncClient()
