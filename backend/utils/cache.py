# utils/cache.py

cache_store = {}

def get_from_cache(video_id: str):
    return cache_store.get(video_id)

def set_cache(video_id: str, result: dict):
    cache_store[video_id] = result
