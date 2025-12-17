from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
from decouple import config

from app.db.session import get_db
from app.models.user import User
from app.core.security import create_access_token

router = APIRouter()


class GoogleLoginRequest(BaseModel):
    credential: str


@router.post("/google")
def login_google(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    try:
        # 1. Verify Google Token
        id_info = id_token.verify_oauth2_token(
            request.credential, requests.Request(), config("GOOGLE_CLIENT_ID")
        )

        # 2. Get User Info
        email = id_info["email"]
        google_id = id_info["sub"]
        name = id_info.get("name")
        picture = id_info.get("picture")

        # 3. Check DB for User
        user = db.query(User).filter(User.email == email).first()

        if not user:
            # Create New User
            user = User(
                email=email,
                google_id=google_id,
                full_name=name,
                profile_picture=picture,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Update existing user info (e.g. if they changed profile pic)
            user.full_name = name
            user.profile_picture = picture
            db.commit()

        # 4. Create Session Token (JWT)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.full_name,
                "picture": user.profile_picture,
            },
        }

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google Token")
