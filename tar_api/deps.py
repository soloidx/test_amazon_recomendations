from contextlib import contextmanager

from typing import Generator

from tar_api.models.database import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
