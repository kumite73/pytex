from fastapi import APIRouter

router: APIRouter = APIRouter(tags=["main"])


@router.get(
    "/",
    description="Returns a welcome message.",
)
async def root():
    return {"message": "Welcome to Pytex!"}


@router.get(
    "/ping",
    description="Returns a ping response.",
)
async def ping():
    return {"status": "ok"}
