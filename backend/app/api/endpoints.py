from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.storage_service import StorageService
from app.services.ai_service import AIService
from app.models.image import ImageGeneration
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/generate")
async def generate_image(
    prompt: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # 1. Initialize Services
    storage_service = StorageService()
    ai_service = AIService()

    try:
        # 2. Upload Input Image to Storage
        input_url = await storage_service.upload_file(image)

        # 3. Create Database Record (Status: Processing)
        db_record = ImageGeneration(
            prompt=prompt, input_image_url=input_url, status="processing"
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        # 4. Call AI Service (In a real app, this might be a background task/queue)
        output_url = await ai_service.generate_image(prompt, input_url)

        # 5. Update Record with Result
        db_record.output_image_url = output_url
        db_record.status = "completed"
        db.commit()

        return {
            "id": db_record.id,
            "status": "completed",
            "input_url": input_url,
            "output_url": output_url,
            "prompt": prompt,
        }

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
