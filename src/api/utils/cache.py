from cachetools import TTLCache, cached
from cachetools.keys import hashkey


stats_cache = TTLCache(maxsize=100, ttl=600)

logs_cache = TTLCache(maxsize=100, ttl=600)

book_id_cache = TTLCache(maxsize=500, ttl=600)
books_cache = TTLCache(maxsize=500, ttl=600)
search_books_cache = TTLCache(maxsize=500, ttl=600)
top_rated_books_cache = TTLCache(maxsize=100, ttl=600)
price_range_books_cache = TTLCache(maxsize=500, ttl=600)

ml_features_cache = TTLCache(maxsize=1000, ttl=600)
ml_training_data_cache = TTLCache(maxsize=1000, ttl=600)
ml_predict_cache = TTLCache(maxsize=1000, ttl=600)

def cache_with_stats(func) -> callable:
    """
    Decorator to cache the result of a function with a TTLCache for statistics.
    This uses a cache with a maximum size of 100 and a TTL of 600 seconds.
    Args:
        func (callable): The function to be cached.
    Returns:
        callable: The cached version of the function.
    """
    return cached(cache=stats_cache)(func)

def cache_with_books(func) -> callable:
    """
    Decorator to cache the result of a function with a TTLCache for books.
    This uses a cache with a maximum size of 500 and a TTL of 600 seconds.
    Args:
        func (callable): The function to be cached.
    Returns:
        callable: The cached version of the function.
    """
    return cached(cache=books_cache)(func)

def cache_with_books_id(func) -> callable:
    """
    Decorator to cache the result of a function with a TTLCache for book IDs.
    This uses a cache with a maximum size of 500 and a TTL of 600 seconds.
    Args:
        func (callable): The function to be cached.
    Returns:
        callable: The cached version of the function.
    """
    return cached(cache=book_id_cache)(func)

def cache_with_search_books(func) -> callable:
    """
    Decorator to cache the result of a function with a TTLCache for search books.
    This uses a cache with a maximum size of 500 and a TTL of 600 seconds.
    Args:
        func (callable): The function to be cached.
    Returns:
        callable: The cached version of the function.
    """
    return cached(cache=search_books_cache)(func)

def cache_with_top_rated_books(func) -> callable:
    """
    Decorator to cache the result of a function with a TTLCache for top-rated books.
    This uses a cache with a maximum size of 100 and a TTL of 600 seconds.
    Args:
        func (callable): The function to be cached.
    Returns:
        callable: The cached version of the function.
    """
    return cached(cache=top_rated_books_cache)(func)

def cache_with_price_range_books(func) -> callable:
    """
    Decorator to cache the result of a function with a TTLCache for price range books.
    This uses a cache with a maximum size of 500 and a TTL of 600 seconds.
    Args:
        func (callable): The function to be cached.
    Returns:
        callable: The cached version of the function.
    """
    return cached(cache=price_range_books_cache)(func)

def cache_with_ml_features(func) -> callable:
    """
    Decorator to cache the result of a function with a TTLCache for ML features.
    This uses a cache with a maximum size of 1000 and a TTL of 600 seconds.
    Args:
        func (callable): The function to be cached.
    Returns:
        callable: The cached version of the function.
    """
    return cached(cache=ml_features_cache)(func)

def cache_with_ml_training_data(func) -> callable:
    """
    Decorator to cache the result of a function with a TTLCache for ML training data.
    This uses a cache with a maximum size of 1000 and a TTL of 600 seconds.
    Args:
        func (callable): The function to be cached.
    Returns:
        callable: The cached version of the function.
    """
    return cached(cache=ml_training_data_cache)(func)


def cache_with_predict(func) -> callable:
    """
    Decorator to cache the result of a function with a TTLCache for predictions.
    This uses a cache with a maximum size of 1000 and a TTL of 600 seconds.
    """
    def key(features):
        # Converte a lista de objetos Pydantic ou dicts para uma tupla hashable
        return hashkey(tuple((f["price"], f["category"]) if isinstance(f, dict) else (f.price, f.category) for f in features))
    
    return cached(cache=ml_predict_cache, key=key)(func)