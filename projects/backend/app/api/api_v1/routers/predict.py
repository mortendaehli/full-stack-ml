from pathlib import Path
from typing import Any, Dict

from app import entities
from app.core import auth
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from imagenet import ImageNet

router = APIRouter()


@router.post("/image")
async def predict_image(
    *,
    file: UploadFile = File(...),
    current_user: entities.User = Depends(auth.get_current_active_user),
) -> Dict[str, Any]:
    valid_suffix = Path(file.filename).suffix.lower() in (".jpg", ".jpeg", ".png")
    print(Path(file.filename).suffix.lower())
    if not valid_suffix:
        raise HTTPException(status_code=409, detail="The following image formats are supported: jpg, jpeg and png.")
    image = ImageNet.parse_image(await file.read())
    predictions = ImageNet().predict(image=image)

    return {
        "filename": file.filename,
        "contenttype": file.content_type,
        "prediction": float(predictions[0]["confidence"]),
        "likely_class": predictions[0]["prediction"],
    }
