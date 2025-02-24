import io
import os

from botocore.client import Config
from dotenv import load_dotenv
from fastapi import UploadFile

load_dotenv()

import boto3

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


class StorageConnector:
    def __init__(self) -> None:
        self.storage_client = boto3.client(
            "s3",
            region_name="ap-northeast-2",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

    async def create_image(self, image: UploadFile):
        contents = await image.read()
        file_like_object = io.BytesIO(contents)
        self.storage_client.upload_fileobj(
            file_like_object,
            "nbbang-images",
            image.filename,
            ExtraArgs={
                "ContentType": "image/webp",
            },
        )

    def delete_image(self, filename):
        self.storage_client.delete_object(Bucket="nbbang-images", Key=filename + ".webp")
