import uuid
from supabase import create_client, Client
from fastapi import UploadFile
from decouple import config
# from app.core.config import settings

class StorageService:
    def __init__(self):
        self.supabase: Client = create_client(config("SUPABASE_URL"), config("SUPABASE_KEY"))
        self.bucket = config("SUPABASE_BUCKET")

    async def upload_file(self, file: UploadFile) -> str:
        # Generate unique filename (Collision avoidance)
        file_ext = file.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_ext}"
        
        # Read file content
        file_content = await file.read()
        
        # Upload to Supabase
        self.supabase.storage.from_(self.bucket).upload(
            path=file_name,
            file=file_content,
            file_options={"content-type": file.content_type}
        )
        
        # Get Public URL
        public_url = self.supabase.storage.from_(self.bucket).get_public_url(file_name)
        return public_url