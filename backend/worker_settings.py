# backend/worker_settings.py
"""ARQ worker settings — Work #3"""
from arq.connections import RedisSettings

from core.config import settings


async def simple_work(ctx: dict, *args, **kwargs) -> str:
    """Display the job data."""
    print("=== simple_work ===")
    print(f"job_id   : {ctx['job_id']}")
    print(f"job_try  : {ctx['job_try']}")
    print(f"args     : {args}")
    print(f"kwargs   : {kwargs}")
    return f"processed args={args} kwargs={kwargs}"


class WorkerSettings:
    functions = [simple_work]
    redis_settings = RedisSettings(
        host=settings.redis_host,
        port=settings.redis_port,
    )