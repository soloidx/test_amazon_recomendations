from fastapi import APIRouter

from tar_api.schema.api_v1 import AddRequest


router = APIRouter(prefix="/v1", tags=["version 1"])


@router.post("/products/add/")
async def add_product(request: AddRequest):
    """
    Adds a amazon url to the system
    """
    return {"success": request.url}
