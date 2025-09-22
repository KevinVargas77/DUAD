from cache_manager import CacheManager
from config import settings
import redis

# Global cache instance
cache_manager = None

def init_cache():
    """Initialize the cache manager"""
    global cache_manager
    
    if not settings.CACHE_ENABLED:
        cache_manager = None
        return
    
    try:
        cache_manager = CacheManager(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD != "REDIS_PASSWORD_PLACEHOLDER" else None,
            db=settings.REDIS_DB
        )
    except redis.RedisError as e:
        # If Redis connection fails, disable caching
        print(f"Warning: Redis connection failed: {e}. Caching disabled.")
        cache_manager = None

def get_cache():
    """Get the cache manager instance"""
    return cache_manager

def is_cache_enabled():
    """Check if caching is enabled and available"""
    return cache_manager is not None