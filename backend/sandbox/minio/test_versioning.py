# backend/sandbox/minio/test_versioning.py
"""Versioning test against MinIO — Work #... (MinIO ข้อ 3b)"""
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
LOCAL_IMAGE_V1 = ASSETS_DIR / "photo_v1.jpg"   # รูปตัวเองรอบแรก
LOCAL_IMAGE_V2 = ASSETS_DIR / "photo_v2.jpg"   # รูปตัวเองรอบสอง (ทับ object name เดิม)

DOWNLOAD_DIR = Path(__file__).resolve().parent / "downloads"


def ensure_bucket(bucket: str):
    """bucket_exists / make_bucket — เช็คว่า bucket มีอยู่ไหม ถ้าไม่มีให้สร้าง"""
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
        print(f"[OK] created bucket '{bucket}'")
    else:
        print(f"[OK] bucket '{bucket}' already exists")


def enable_versioning(bucket: str):
    """set_bucket_versioning — เปิด object versioning ให้ bucket"""
    client.set_bucket_versioning(bucket, VersioningConfig(ENABLED))
    status = client.get_bucket_versioning(bucket).status
    print(f"[OK] versioning status of '{bucket}' = {status}")


def upload_file(bucket: str, object_name: str, file_path: Path) -> str:
    """fput_object — อัปโหลดไฟล์จาก local path ขึ้น bucket, คืน version_id ที่ MinIO สร้างให้"""
    result = client.fput_object(bucket, object_name, str(file_path))
    print(f"[OK] uploaded '{file_path.name}' -> {bucket}/{object_name} (version_id={result.version_id})")
    return result.version_id


def download_file(bucket: str, object_name: str, dest_path: Path, version_id: str | None = None):
    """fget_object — ดาวน์โหลดไฟล์ลง local path; ถ้าระบุ version_id จะได้ version นั้นแทนตัวล่าสุด"""
    client.fget_object(bucket, object_name, str(dest_path), version_id=version_id)
    label = version_id or "latest"
    print(f"[OK] downloaded {bucket}/{object_name} (version={label}) -> {dest_path}")


def list_versions(bucket: str, object_name: str):
    """list_objects(..., include_version=True) — แสดง version ทั้งหมดของ object นี้"""
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

    # อัปโหลดรูปที่ 1 และรูปที่ 2 ทับ object name เดิม -> เกิด version ใหม่ทุกครั้ง
    v1_id = upload_file(BUCKET, OBJECT_NAME, LOCAL_IMAGE_V1)
    v2_id = upload_file(BUCKET, OBJECT_NAME, LOCAL_IMAGE_V2)

    list_versions(BUCKET, OBJECT_NAME)  # ไว้ screenshot ตอนเขียนรายงาน

    DOWNLOAD_DIR.mkdir(exist_ok=True)

    # กรณีที่ 1: ไม่ระบุ version -> ได้รูปล่าสุด (รูปที่ 2)
    download_file(BUCKET, OBJECT_NAME, DOWNLOAD_DIR / "latest.jpg")

    # กรณีที่ 2: ระบุ version_id ของรูปแรก (v1_id ที่ได้ตอน upload / ตรงกับที่เห็นใน list_objects) -> ได้รูปเก่า (รูปที่ 1)
    download_file(BUCKET, OBJECT_NAME, DOWNLOAD_DIR / "oldest.jpg", version_id=v1_id)

    print(f"\n[SUMMARY] v1_id={v1_id}  v2_id={v2_id}")


if __name__ == "__main__":
    main()
