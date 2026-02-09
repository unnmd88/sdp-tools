from httpx import AsyncClient


async def fetch_controller(client: AsyncClient):
    res = await client.get(
        "http://192.168.35.34:8089/api/v2/controllers/ext:690066/status"
    )
    # print(res.json())
    return res
