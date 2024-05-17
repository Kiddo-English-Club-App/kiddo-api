import os
import boto3
from botocore.exceptions import ClientError

from settings.environment import env
from shared.app_context import AppContext
from shared.exceptions import NotFound, Unauthorized
from services.application.file_service import File
from ..application.file_service import FileService


class S3FileService(FileService):


    def __init__(self, app_context: AppContext):
        self.client = boto3.client(
            service_name ="s3",
            endpoint_url = env.S3_ENDPOINT_URL,
            aws_access_key_id = env.S3_ACCESS_KEY_ID,
            aws_secret_access_key = env.S3_SECRET_KEY,
            region_name=env.S3_REGION_NAME, # Must be one of: wnam, enam, weur, eeur, apac, auto
        )
        self.app_context = app_context

    def get_file(self, file_name: str) -> File:
        #if not self.app_context.authenticated():
        #    raise Unauthorized("Not authenticated")
        
        if os.path.exists(f"cache/{file_name}"):
            with open(f"cache/{file_name}", "rb") as file:
                print("Cache hit")
                content = file.read()
                mime_type = self.get_mime_type(file_name)
                return File(file_name, content, mime_type)
        try:
            s3_object = self.client.get_object(Bucket=env.S3_BUCKET_NAME, Key=file_name)
            content = s3_object["Body"].read()
            mime_type = s3_object["ContentType"]
            self.cache_file(file_name, content)
            return File(file_name, content, mime_type)
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise NotFound("File not found")
            raise e
    
    
