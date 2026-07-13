from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, UploadFile, HTTPException

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

UPLOAD_DIR = Path("uploads/posters")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


@router.post("/poster")
async def upload_poster(
    file: UploadFile = File(...)
):

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Можна завантажувати тільки зображення",
        )

    extension = Path(file.filename).suffix

    filename = f"{uuid4()}{extension}"

    filepath = UPLOAD_DIR / filename

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "poster_url": f"/uploads/posters/{filename}"
    }