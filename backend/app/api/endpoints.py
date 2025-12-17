# from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
# from sqlalchemy.orm import Session
# from pydantic import BaseModel
# from app.db.session import get_db
# from app.services.storage_service import StorageService
# from app.services.ai_service import AIService
# from app.models.image import ImageGeneration
# from app.db.base import Base
# from app.db.session import engine
# from app.services.auth_service import AuthService
# from app.api.deps import get_current_user
# from app.models.user import User

# Base.metadata.create_all(bind=engine)

# router = APIRouter()


# @router.post("/generate")
# async def generate_image(
#     prompt: str = Form(...),
#     self_image: UploadFile = File(...),   # <--- New Input
#     target_image: UploadFile = File(...), # <--- New Input
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     storage_service = StorageService()
#     ai_service = AIService()

#     try:
#         # 1. Upload BOTH images to Supabase Storage
#         self_image_url = await storage_service.upload_file(self_image)
#         target_image_url = await storage_service.upload_file(target_image)

#         # 2. Save Metadata to DB
#         db_record = ImageGeneration(
#             user_id=current_user.id,
#             prompt=prompt,
#             self_image_url=self_image_url,     # Save URL 1
#             target_image_url=target_image_url, # Save URL 2
#             status="processing"
#         )
#         db.add(db_record)
#         db.commit()
#         db.refresh(db_record)

#         # 3. Call AI (Mocked for now)
#         # We pass both URLs to the AI service
#         output_url = await ai_service.generate_image(prompt, self_image_url) 

#         # 4. Update DB with Result
#         db_record.output_image_url = output_url
#         db_record.status = "completed"
#         db.commit()

#         return {
#             "id": db_record.id,
#             "status": "completed",
#             "self_image_url": self_image_url,
#             "target_image_url": target_image_url,
#             "output_url": output_url
#         }

#     except Exception as e:
#         print(f"Error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# # Input Schema
# class GoogleLoginRequest(BaseModel):
#     credential: str  # This is the token string Google gives the Frontend


# # ... inside your existing router ...


# @router.post("/auth/google")
# def login_google(request: GoogleLoginRequest, db: Session = Depends(get_db)):
#     auth_service = AuthService()
#     result = auth_service.login_user(db, request.credential)

#     if not result:
#         raise HTTPException(status_code=400, detail="Invalid Google Token")

#     return result
