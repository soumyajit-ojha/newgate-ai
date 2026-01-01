import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


# from app.core.config import settings
# from app.api.endpoints import router
from app.api import auth, generate

app = FastAPI(title="Newgate AI")

protocol = config("HOST_PROTOCOL", default="http")
ip = config("HOST_IP")
port = config("HOST_PORT", default="8000")

origins = [
    "http://localhost:5173",  # For Local Development
    "http://127.0.0.1:5173",  # For Local Development
    "https://newgate-ai.vercel.app",  # THIS IS ACTUAL VERCEL OR MAIN DOMAIN
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
