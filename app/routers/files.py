from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_files():
    return [{"id": 1, "filename": "example.pdf"}]
