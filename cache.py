import time
from typing import Any, Optional, Callable
from datetime import datetime, timedelta


class InMemoryCache:
    def __init__(self, ttl_hours: float = 12):
        self.ttl = ttl_hours * 3600
        self._cache = {}
        self._timestamps = {}
    
    def get(self, key: str, fetcher: Callable[[], Any]) -> Any:
        current_time = time.time()
        
        if key in self._cache and key in self._timestamps:
            if current_time - self._timestamps[key] < self.ttl:
                return self._cache[key]
        
        data = fetcher()
        self._cache[key] = data
        self._timestamps[key] = current_time
        return data
    
    def invalidate(self, key: Optional[str] = None):
        if key:
            self._cache.pop(key, None)
            self._timestamps.pop(key, None)
        else:
            self._cache.clear()
            self._timestamps.clear()
    
    def is_cached(self, key: str) -> bool:
        if key not in self._cache:
            return False
        current_time = time.time()
        return current_time - self._timestamps.get(key, 0) < self.ttl
    
    def get_cache_info(self, key: str) -> dict:
        if key not in self._cache:
            return {"cached": False}
        
        timestamp = self._timestamps.get(key, 0)
        current_time = time.time()
        age = current_time - timestamp
        expires_in = max(0, self.ttl - age)
        
        return {
            "cached": True,
            "cached_at": datetime.fromtimestamp(timestamp).isoformat(),
            "expires_at": datetime.fromtimestamp(timestamp + self.ttl).isoformat(),
            "age_seconds": age,
            "expires_in_seconds": expires_in
        }