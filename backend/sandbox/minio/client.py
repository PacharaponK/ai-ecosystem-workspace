# backend/sandbox/minio/client.py
"""MinIO client — Work #... (MinIO #3)"""
from minio import Minio

from core.config import settings

client = Minio(
    settings.minio_endpoint,
    access_key=settings.minio_root_user,
    secret_key=settings.minio_root_password,
    secure=settings.minio_secure,
)
