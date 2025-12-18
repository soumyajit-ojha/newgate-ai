import uuid
from supabase import create_client, Client
from fastapi import UploadFile, HTTPException
from decouple import config

# from app.core.config import settings


class StorageService:
    def __init__(self):
        self.supabase: Client = create_client(
            config("SUPABASE_URL"), config("SUPABASE_KEY")
        )
        self.bucket = config("SUPABASE_BUCKET")
        self.MAX_FILE_SIZE = 10 * 1024 * 1024

    async def upload_file(self, file: UploadFile, folder: str = "uploads") -> str:
        """
        Uploads a file to Supabase Storage and returns the Public URL.
        """
        try:
            # Read file content
            file_content = await file.read()
            if len(file_content) > self.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=413,  # 413 = Payload Too Large
                    detail=f"File {file.filename} exceeds the 10MB limit.",
                )
            file_ext = file.filename.split(".")[-1]
            file_name = f"{folder}/{uuid.uuid4()}.{file_ext}"

            # Upload to Supabase
            self.supabase.storage.from_(self.bucket).upload(
                path=file_name,
                file=file_content,
                file_options={"content-type": file.content_type},
            )

            # Get Public URL
            public_url = self.supabase.storage.from_(self.bucket).get_public_url(
                file_name
            )
            return public_url
        except Exception as e:
            print(f"Storage Upload Error: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Failed to upload image to storage"
            )
