from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from decouple import config

# from app.core.config import settings
# from app.api.endpoints import router
from app.api import auth, generate

app = FastAPI(title="Newgate AI")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# CORS Configuration (Essential for React Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(generate.router, prefix="/api/image")


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Newgate AI Backend"}
