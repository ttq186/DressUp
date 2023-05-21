import bcrypt
from fastapi.concurrency import run_in_threadpool


def _hash_password_sync(password: str) -> bytes:
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


async def hash_password(password: str) -> bytes:
    return await run_in_threadpool(_hash_password_sync, password)


def _check_password_sync(password: str, hashed_password: bytes) -> bool:
    password_bytes = bytes(password, "utf-8")
    return bcrypt.checkpw(password_bytes, hashed_password)


async def check_password(password: str, hashed_password: bytes) -> bool:
    return await run_in_threadpool(_check_password_sync, password, hashed_password)
