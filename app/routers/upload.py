from fastapi import APIRouter, File, UploadFile, HTTPException
import cloudinary
import cloudinary.uploader

from app.core.config import settings

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


@router.post("/poster")
async def upload_poster(file: UploadFile = File(...)):

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400,detail="Можна завантажувати тільки зображення")

    result = cloudinary.uploader.upload(file.file)

    return {
        "poster_url": result["secure_url"]
    }