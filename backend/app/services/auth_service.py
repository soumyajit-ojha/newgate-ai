from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.orm import Session
# from app.core.config import settings
from app.models.user import User
from app.core.security import create_access_token
from decouple import config


class AuthService:
    def verify_google_token(self, token: str):
        try:
            # Verify the token with Google's public keys
            id_info = id_token.verify_oauth2_token(
                token, requests.Request(), config("GOOGLE_CLIENT_ID")
            )
            return id_info
        except ValueError:
            return None

    def get_or_create_user(self, db: Session, google_data: dict):
        # Check if user exists by Google ID (sub)
        user = db.query(User).filter(User.google_id == google_data["sub"]).first()

        if not user:
            # Create new user
            user = User(
                email=google_data["email"],
                google_id=google_data["sub"],
                full_name=google_data.get("name"),
                profile_picture=google_data.get("picture"),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Optional: Update profile pic if changed
            user.profile_picture = google_data.get("picture")
            db.commit()

        return user

    def login_user(self, db: Session, token: str):
        # 1. Verify Google Token
        google_data = self.verify_google_token(token)
        if not google_data:
            return None

        # 2. Sync with Database
        user = self.get_or_create_user(db, google_data)

        # 3. Generate Our App's Token
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
