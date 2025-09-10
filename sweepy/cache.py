import time
from functools import wraps


def timed_cached_property(ttl_seconds: int):
    """
    Decorator to cache a property for a specified time-to-live (TTL) in seconds.
    After the TTL expires, the property will be recomputed.
    """

    if ttl_seconds <= 0 or not isinstance(ttl_seconds, int):
        raise ValueError("TTL must be an integer greater than 0 seconds")

    def decorator(func):
        attr_name = f"_cached_{func.__name__}"
        time_name = f"_cached_time_{func.__name__}"

        @property
        @wraps(func)
        def wrapper(self):
            current_time = time.time()
            cached_time = getattr(self, time_name, None)
            cached_value = getattr(self, attr_name, None)

            if cached_time is None or (current_time - cached_time) > ttl_seconds:
                cached_value = func(self)
                setattr(self, attr_name, cached_value)
                setattr(self, time_name, current_time)
            return cached_value

        return wrapper

    return decorator


def timed_cache(ttl_seconds: int):
    """
    Decorator to cache the result of a function for a specified time-to-live (TTL) in seconds.
    After the TTL expires, the function will be recomputed.
    """

    if ttl_seconds <= 0 or not isinstance(ttl_seconds, int):
        raise ValueError("TTL must be an integer greater than 0 seconds")

    def decorator(func):
        cache = {}
        last_update = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            key = (args, frozenset(kwargs.items()))

            if key not in cache or (current_time - last_update[key]) > ttl_seconds:
                cache[key] = func(*args, **kwargs)
                last_update[key] = current_time

            return cache[key]

        return wrapper

    return decorator
