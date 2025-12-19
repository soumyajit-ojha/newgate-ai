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

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost",
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


# --- SERVE FRONTEND (Final Step) ---
# Construct the absolute path to the frontend dist directory
frontend_dist_path = Path(__file__).parent.parent.parent / "frontend" / "dist"

if frontend_dist_path.exists():

    # 2. Mount the 'assets' folder explicitly
    # React (Vite) puts all JS/CSS in the /assets folder. We serve these directly.
    assets_path = frontend_dist_path / "assets"
    if assets_path.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")

    # 3. Define a Catch-All Route
    # This captures ANY path that wasn't handled by the API or /assets above
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # Security: Don't hijack API routes that return 404
        if full_path.startswith("api"):
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="API Endpoint not found")

        # Check if a specific file exists (e.g., favicon.ico, robots.txt)
        file_path = frontend_dist_path / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)

        # SPA FALLBACK: If file doesn't exist, return index.html
        # This allows React Router to handle /dashboard, /login, etc.
        return FileResponse(frontend_dist_path / "index.html")

else:
    print(f"Warning: Frontend build not found at {frontend_dist_path}")
