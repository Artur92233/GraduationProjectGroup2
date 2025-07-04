import aioboto3
from fastapi import UploadFile
from settings import settings


class S3Storage:
    def __init__(self):
        self.bucket_name = settings.BUCKET_NAME

    async def get_s3_session(self):
        session = aioboto3.Session()
        async with session.client(
            "s3",
            endpoint_url=settings.ENDPOINT,
            aws_access_key_id=settings.ACCESS_KEY,
            aws_secret_access_key=settings.SECRET_KEY,
            region_name="EEUR",
        ) as s3:
            yield s3

    async def upload_new_buildings_image(self, file: UploadFile, new_buildings_uuid: str) -> str:
        async for s3_client in self.get_s3_session():
            path = f"products/{new_buildings_uuid}/{file.filename}"
            await s3_client.upload_fileobj(file, self.bucket_name, path)
            url = f"{settings.PUBLIC_URL}/{path}"
        return url


s3_storage = S3Storage()