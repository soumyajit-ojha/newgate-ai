import uuid
import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile, HTTPException
from decouple import config

# from app.core.config import settings


class StorageService:
    def __init__(self):
        self.bucket_name = config("S3_BUCKET_NAME")
        self.region = config("AWS_REGION")
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
            region_name=self.region,
        )
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
            file_key = f"{folder}/{uuid.uuid4()}.{file_ext}"

            await file.seek(0)

            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=file_content,
                ContentType=file.content_type,
                # ACL='public-read' is not needed if Bucket Policy is set,
                # but good to ensure accessibility if settings change.
            )
            public_url = (
                f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{file_key}"
            )

            # Upload to Supabase
            # self.supabase.storage.from_(self.bucket).upload(
            #     path=file_name,
            #     file=file_content,
            #     file_options={"content-type": file.content_type},
            # )

            # Get Public URL
            # public_url = self.supabase.storage.from_(self.bucket).get_public_url(
            #     file_name
            # )
            return public_url

        except NoCredentialsError:
            raise HTTPException(status_code=500, detail="AWS Credentials missing")

        except Exception as e:
            print(f"Storage Upload Error: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Failed to upload image to storage"
            )
