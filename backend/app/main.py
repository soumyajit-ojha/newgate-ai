from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
# from app.core.config import settings
from app.api.endpoints import router

app = FastAPI(title="Newgate AI")

# CORS Configuration (Essential for React Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change this to your Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/API")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Newgate AI Backend"}