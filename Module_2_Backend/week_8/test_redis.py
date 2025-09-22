import sys
sys.path.append('fruits_api')

from cache import init_cache, get_cache, is_cache_enabled

def test_redis_connection():
    print("Starting Redis connection test...")
    
    # Initialize cache
    init_cache()
    
    # Check if enabled
    if not is_cache_enabled():
        print("ERROR: Cache is not enabled or could not connect")
        return
    
    print("SUCCESS: Redis connection successful!")
    
    # Get cache instance
    cache = get_cache()
    
    # Test basic operations
    test_key = "test_key"
    test_value = {"message": "Hello Redis!", "data": [1, 2, 3]}
    
    print(f"Storing data in Redis with key '{test_key}'...")
    result = cache.store_data(test_key, test_value, 60)  # TTL of 60 seconds
    
    if result:
        print("SUCCESS: Data stored successfully")
    else:
        print("ERROR: Failed to store data")
        return
    
    print(f"Checking existence of key '{test_key}'...")
    exists, ttl = cache.check_key(test_key)
    
    if exists:
        print(f"SUCCESS: Key exists. TTL: {ttl} seconds")
    else:
        print("ERROR: Key does not exist")
        return
    
    print(f"Retrieving data from key '{test_key}'...")
    retrieved_data = cache.get_data(test_key)
    
    if retrieved_data:
        print(f"SUCCESS: Data retrieved: {retrieved_data}")
    else:
        print("ERROR: Could not retrieve data")
        return
    
    print(f"Deleting key '{test_key}'...")
    deleted = cache.delete_data(test_key)
    
    if deleted:
        print("SUCCESS: Key deleted successfully")
    else:
        print("ERROR: Failed to delete key")
    
    print("\nAll Redis tests completed successfully!")

if __name__ == "__main__":
    test_redis_connection()