from typing import List, Set
import redis  # type: ignore

from settings import settings


def get_connection():
    conn = redis.from_url(settings.REDIS_URL)
    return conn


def increase_keys_for_product(asin: str, keys: Set):
    redis = get_connection()

    for key in keys:
        redis.zincrby(asin, 1, key)


def get_top_keys_from_product(asin: str) -> List:
    redis = get_connection()
    keys = redis.zrange(asin, 0, 10, desc=True)
    return [x.decode() for x in keys]
