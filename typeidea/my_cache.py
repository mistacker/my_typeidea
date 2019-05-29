import functools

from .my_lrucache import LRUCacheDict


def cache_it(max_size=1024, expiration=60):
    CACHE = LRUCacheDict(max_size, expiration)

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            key = repr(*args, **kwargs)
            result = CACHE[key]
            if not result:
                result = func(*args, **kwargs)
                CACHE[key] = result
            return result

        return inner

    return wrapper

# from functools import lru_cache

