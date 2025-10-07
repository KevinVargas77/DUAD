# Cache Decorators - Advanced Caching with Filters Support
from functools import wraps
from flask import request, jsonify
from cache import get_cache, is_cache_enabled
from config import settings
import hashlib

def cache_key_generator(base_key, filters=None):
    """Generate a cache key that includes filters"""
    if not filters:
        return base_key
    
    # Sort filters to ensure consistent key generation
    filter_parts = []
    for key, value in sorted(filters.items()):
        if value is not None:
            filter_parts.append(f"{key}={value}")
    
    if filter_parts:
        filter_string = "_".join(filter_parts)
        return f"{base_key}_{filter_string}"
    
    return base_key

def invalidate_cache_pattern(pattern):
    """Invalidate all cache keys matching a pattern"""
    if not is_cache_enabled():
        return
    
    cache = get_cache()
    if cache:
        cache.delete_data_with_pattern(pattern)

def cached_response(base_cache_key, ttl=None):
    """
    Decorator for caching GET responses with filter support
    
    Args:
        base_cache_key: Base key for cache (e.g., "all_products", "product")
        ttl: Time to live in seconds (uses default from config if None)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Only cache GET requests
            if request.method != 'GET':
                return func(*args, **kwargs)
            
            # Skip caching if disabled
            if not is_cache_enabled():
                return func(*args, **kwargs)
            
            cache = get_cache()
            if not cache:
                return func(*args, **kwargs)
            
            # Extract filters from request args
            filters = {}
            for key, value in request.args.items():
                if value:  # Only include non-empty values
                    filters[key] = value
            
            # Generate cache key with filters
            cache_key = cache_key_generator(base_cache_key, filters)
            
            # Add any URL parameters (like product_id) to the cache key
            if kwargs:
                param_parts = []
                for key, value in sorted(kwargs.items()):
                    param_parts.append(f"{key}={value}")
                if param_parts:
                    cache_key = f"{cache_key}_{'_'.join(param_parts)}"
            
            # Try to get from cache
            cached_data = cache.get_data(cache_key)
            if cached_data is not None:
                # Return cached response with proper JSON format
                return jsonify(cached_data), 200
            
            # Execute original function
            response = func(*args, **kwargs)
            
            # Cache successful responses
            if hasattr(response, 'status_code') and response.status_code == 200:
                try:
                    # Extract JSON data from response
                    response_data = response.get_json()
                    
                    # Store in cache
                    cache_ttl = ttl or settings.CACHE_DEFAULT_TTL
                    cache.store_data(cache_key, response_data, cache_ttl)
                except Exception:
                    # If we can't cache, just return the original response
                    pass
            
            return response
        
        return wrapper
    return decorator

def invalidate_cache_on_change(cache_patterns):
    """
    Decorator to invalidate cache after CUD operations
    
    Args:
        cache_patterns: List of cache patterns to invalidate (e.g., ["all_products*", "product*"])
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute the original function
            response = func(*args, **kwargs)
            
            # Invalidate cache only if operation was successful
            if hasattr(response, 'status_code') and response.status_code in [200, 201]:
                for pattern in cache_patterns:
                    invalidate_cache_pattern(pattern)
            
            return response
        
        return wrapper
    return decorator