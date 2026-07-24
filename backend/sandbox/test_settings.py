import sys
from pathlib import Path

# Add 'backend' (parent of this sandbox/ dir) to the path so 'core' resolves
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.config import settings


def main() -> None:
    """Print settings configuration to verify correct loading from the environment."""
    print("=== PostgreSQL ===")
    print(f"postgres_user     = {settings.postgres_user}")
    
    # Mask password for security when outputting to logs/terminal
    postgres_pass = settings.postgres_password
    masked_password = f"{postgres_pass[:3]}***" if len(postgres_pass) > 3 else "***"
    print(f"postgres_password = {masked_password}")
    
    print(f"postgres_db       = {settings.postgres_db}")
    print(f"postgres_host     = {settings.postgres_host}")
    print(f"postgres_port     = {settings.postgres_port}")

    print("\n=== Redis ===")
    print(f"redis_host = {settings.redis_host}")
    print(f"redis_port = {settings.redis_port}")

    print("\n=== Label Studio ===")
    print(f"label_studio_url     = {settings.label_studio_url}")
    print(f"label_studio_api_key = {settings.label_studio_api_key}")

    print("\n=== Computed ===")
    print(f"database_url = {settings.database_url}")


if __name__ == "__main__":
    main()