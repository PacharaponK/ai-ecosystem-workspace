# backend/sandbox/minio/test_versioning.py
"""Versioning test against MinIO — Work #... (MinIO #3b)"""
import sys
from pathlib import Path

# Add 'backend' (parent.parent.parent of this sandbox/minio/ dir) to the path so 'core' resolves
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from minio.commonconfig import ENABLED
from minio.versioningconfig import VersioningConfig

from client import client

BUCKET = "photos"
OBJECT_NAME = "me.jpg"

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
LOCAL_IMAGE_V1 = ASSETS_DIR / "photo_v1.jpg"   # First photo
LOCAL_IMAGE_V2 = ASSETS_DIR / "photo_v2.jpg"   # Second photo (overwrites the same object name)

DOWNLOAD_DIR = Path(__file__).resolve().parent / "downloads"


def ensure_bucket(bucket: str):
    """bucket_exists / make_bucket — check whether the bucket exists, create it if not"""
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
        print(f"[OK] created bucket '{bucket}'")
    else:
        print(f"[OK] bucket '{bucket}' already exists")


def enable_versioning(bucket: str):
    """set_bucket_versioning — turn on object versioning for the bucket"""
    client.set_bucket_versioning(bucket, VersioningConfig(ENABLED))
    status = client.get_bucket_versioning(bucket).status
    print(f"[OK] versioning status of '{bucket}' = {status}")


def upload_file(bucket: str, object_name: str, file_path: Path) -> str:
    """fput_object — upload a file into the bucket, returning the version_id MinIO assigns"""
    result = client.fput_object(bucket, object_name, str(file_path))
    print(f"[OK] uploaded '{file_path.name}' -> {bucket}/{object_name} (version_id={result.version_id})")
    return result.version_id


def download_file(bucket: str, object_name: str, dest_path: Path, version_id: str | None = None):
    """fget_object — download to a local path; pass version_id to get that version instead of the latest"""
    client.fget_object(bucket, object_name, str(dest_path), version_id=version_id)
    label = version_id or "latest"
    print(f"[OK] downloaded {bucket}/{object_name} (version={label}) -> {dest_path}")


def list_versions(bucket: str, object_name: str):
    """list_objects(..., include_version=True) — list every version of this object"""
    print(f"=== versions of {bucket}/{object_name} ===")
    versions = []
    for obj in client.list_objects(bucket, prefix=object_name, include_version=True):
        if obj.object_name != object_name:
            continue
        print(f"version_id={obj.version_id}  is_latest={obj.is_latest}  last_modified={obj.last_modified}")
        versions.append(obj)
    return versions


def main():
    ensure_bucket(BUCKET)
    enable_versioning(BUCKET)

    # Upload photo 1 then photo 2 over the same object name -> a new version each time
    v1_id = upload_file(BUCKET, OBJECT_NAME, LOCAL_IMAGE_V1)
    v2_id = upload_file(BUCKET, OBJECT_NAME, LOCAL_IMAGE_V2)

    list_versions(BUCKET, OBJECT_NAME)  # for the report screenshot

    DOWNLOAD_DIR.mkdir(exist_ok=True)

    # Case 1: no version given -> returns the latest photo (photo 2)
    download_file(BUCKET, OBJECT_NAME, DOWNLOAD_DIR / "latest.jpg")

    # Case 2: version_id of the first photo (v1_id from the upload, same id shown by
    # list_objects) -> returns the older photo (photo 1)
    download_file(BUCKET, OBJECT_NAME, DOWNLOAD_DIR / "oldest.jpg", version_id=v1_id)

    print(f"\n[SUMMARY] v1_id={v1_id}  v2_id={v2_id}")


if __name__ == "__main__":
    main()
