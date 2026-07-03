from fastapi import APIRouter

router: APIRouter = APIRouter(prefix="/hw1", tags=["hw1"])


@router.get(
    "/",
    description="Returns a welcome message to HW1.",
)
async def hw1_root():
    return {"message": "Welcome to HW1!"}
