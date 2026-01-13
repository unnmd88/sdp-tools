from fastapi import APIRouter, Depends
from httpx import AsyncClient

router = APIRouter(
    prefix="/api-dir",
    tags=["Dir public api"],
)


@router.get(
    "controller-status/{name}",
    # response_model=RegionSchema,
    # status_code=status.HTTP_200_OK,
)
async def fetch_controller_status(
    name: str,
):
    async with AsyncClient() as client:
        client.headers.update(
            {
                "Authorization": "Bearer eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiWVNoaWxvdiIsIm5hbWVpZCI6IjI5IiwibmJmIjoxNzY3MDc3OTg2LCJleHAiOjE3NjcxNjQzODYsImlzcyI6IlJNU0RJUiBJc3N1ZXIiLCJhdWQiOiJSTVNESVIgQXVkaWVuY2UifQ.8dgDgBfmHvaABzyoFzEePPOfHUtB37gNTj_4l64SdSZtsIYOPW3DNkbmU7r8X4NMU5Jy6-aTiTpKePhe4ZUK1Q"
            }
        )
        res = await client.get(
            f"http://192.168.35.34:8089/api/v2/controllers/ext:{name}"
        )
        return res.json()
        print(res)
