from cachetools import TTLCache, cached

default_cache = TTLCache(maxsize=500, ttl=600)
def cache_with_default(func):
    """
    Decorator to cache the result of a function with a default TTLCache.
    This uses a default cache with a maximum size of 500 and a TTL of 600 seconds.
    Args:
        func (callable): The function to be cached.
    Returns:
        callable: The cached version of the function.
    """
    return cached(cache=default_cache)(func)
