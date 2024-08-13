from functools import lru_cache

def llm_cache(maxsize=None, typed=False):

    def decorator(func):
        @lru_cache(maxsize=maxsize, typed=typed)
        def wrapper(*args, **kwargs):
            if kwargs.get('temperature', 0) == 0:
                return func(*args, **kwargs)
            else:
                return func(*args, **kwargs, _no_cache=True)
        
        # Attach cache_clear and cache_info methods to the wrapper
        wrapper.cache_clear = wrapper.cache_clear
        wrapper.cache_info = wrapper.cache_info
        
        return wrapper

    return decorator