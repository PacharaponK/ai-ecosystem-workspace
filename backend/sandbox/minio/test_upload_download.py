# backend/sandbox/minio/test_upload_download.py
"""Basic upload/download test against MinIO — Work #... (MinIO #3a)"""
import sys
from pathlib import Path

# Add 'backend' (parent.parent.parent of this sandbox/minio/ dir) to the path so 'core' resolves
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from client import client

BUCKET = "photos"
OBJECT_NAME = "me.jpg"

LOCAL_IMAGE = Path(__file__).resolve().parent / "assets" / "photo_v1.jpg"
DOWNLOAD_DIR = Path(__file__).resolve().parent / "downloads"


def ensure_bucket(bucket: str):
    """bucket_exists / make_bucket — check whether the bucket exists, create it if not"""
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
        print(f"[OK] created bucket '{bucket}'")
    else:
        print(f"[OK] bucket '{bucket}' already exists")


def upload_file(bucket: str, object_name: str, file_path: Path) -> str:
    """fput_object — upload a file from a local path into the bucket"""
    result = client.fput_object(bucket, object_name, str(file_path))
    print(f"[OK] uploaded '{file_path.name}' -> {bucket}/{object_name} (version_id={result.version_id})")
    return result.version_id


def download_file(bucket: str, object_name: str, dest_path: Path):
    """fget_object — download the object to a local path"""
    client.fget_object(bucket, object_name, str(dest_path))
    print(f"[OK] downloaded {bucket}/{object_name} -> {dest_path}")


def main():
    print("=== bucket_exists / make_bucket ===")
    ensure_bucket(BUCKET)

    print("\n=== fput_object / fget_object ===")
    upload_file(BUCKET, OBJECT_NAME, LOCAL_IMAGE)
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    download_file(BUCKET, OBJECT_NAME, DOWNLOAD_DIR / "basic_download.jpg")


if __name__ == "__main__":
    main()
