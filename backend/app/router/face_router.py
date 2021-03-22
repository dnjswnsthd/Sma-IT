from fastapi import APIRouter

from utils.mask import mask_check


router = APIRouter()


@router.get("/{img_path:path}")
async def mask_checking(img_path: str):
    print(img_path)
    mask_data = mask_check(img_path)
    return mask_data
