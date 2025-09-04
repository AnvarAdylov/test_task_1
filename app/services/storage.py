from minio import Minio

from app.config import settings


def get_minio() -> Minio:
    return Minio(
        settings.S3_ENDPOINT.replace("http://", "").replace("https://", ""),
        access_key=settings.S3_ACCESS_KEY,
        secret_key=settings.S3_SECRET_KEY,
        secure=settings.S3_ENDPOINT.startswith("https://"),
    )


def ensure_bucket(client: Minio, bucket: str):
    found = client.bucket_exists(bucket)
    if not found:
        client.make_bucket(bucket)
