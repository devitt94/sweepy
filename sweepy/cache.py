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
