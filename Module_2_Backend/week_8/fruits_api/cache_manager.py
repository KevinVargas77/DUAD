import redis
import json


class CacheManager:
    def __init__(self, host, port, password=None, *args, **kwargs):
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            password=password,
            decode_responses=True,  # This ensures strings are returned instead of bytes
            *args,
            **kwargs,
        )
        try:
            connection_status = self.redis_client.ping()
            if connection_status:
                # Connection successful but no print as requested
                pass
        except redis.RedisError as error:
            # Re-raise the error so the application can handle it
            raise error

    def store_data(self, key, value, time_to_live=None):
        """Store data in Redis with optional TTL"""
        try:
            # Convert value to JSON string if it's not already a string
            if not isinstance(value, str):
                value = json.dumps(value)
            
            if time_to_live is None:
                self.redis_client.set(key, value)
            else:
                self.redis_client.setex(key, time_to_live, value)
            
            return True
        except redis.RedisError:
            return False

    def check_key(self, key):
        """Check if key exists and return TTL info"""
        try:
            key_exists = self.redis_client.exists(key)
            if key_exists:
                ttl = self.redis_client.ttl(key)
                return True, ttl
            return False, None
        except redis.RedisError:
            return False, None

    def get_data(self, key):
        """Retrieve data from Redis"""
        try:
            output = self.redis_client.get(key)
            if output is not None:
                try:
                    # Try to parse as JSON, if it fails return as string
                    return json.loads(output)
                except json.JSONDecodeError:
                    return output
            return None
        except redis.RedisError:
            return None

    def delete_data(self, key):
        """Delete a specific key from Redis"""
        try:
            output = self.redis_client.delete(key)
            return output == 1
        except redis.RedisError:
            return False

    def delete_data_with_pattern(self, pattern):
        """Delete all keys matching a pattern"""
        try:
            deleted_count = 0
            for key in self.redis_client.scan_iter(match=pattern):
                if self.delete_data(key):
                    deleted_count += 1
            return deleted_count
        except redis.RedisError:
            return 0