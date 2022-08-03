import redis

from app.core.config import get_config_settings

settings = get_config_settings()


def get_redis():
    redis_instance = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        encoding="utf-8",
        # decode_responses=True
    )
    try:
        yield redis_instance
    finally:
        redis_instance.close()

# def redis_cache(cache_key_str: str, expiration: timedelta = None):
#     """
#     Decorator for FastAPI controllers to cache the responses using redis.
#     This needs to be specified AFTER the @router.get fastapi decorator.
#     The controller needs to have `background_tasks: BackgroundTasks`
#     as an argument or this will raise an exception.
#     :param cache_key_str: first argument of the @redis_cache. Is the
#                           key that redis will use to store the data.
#                           The arguments of the controller can be used
#                           to template the key and make it dynamic.
#                           For example: "listview_{crm_object}_{user.id}",
#                           where crm_object and user are arguments of
#                           the controller.
#     :param expiration: timedelta of the expiration of the cache
#     """
#
#     def actual_decorator(func):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             # Build the cache key
#             cache_key = compile_template(cache_key_str, *args, **kwargs)
#
#             reset_cache = kwargs.get('reset_cache', False)
#             if reset_cache:
#                 await redis_client.delete(cache_key)
#             else:
#                 # Check if the cache key is in the cache
#                 data = await redis_client.get(cache_key)
#                 if data:
#                     # Return the cached response
#                     return data
#
#             # Run the wrapped function
#             func_result = await func(*args, **kwargs)
#             # Set the response in the background.
#             if 'background_tasks' in kwargs:
#                 redis_client.set_in_background(kwargs.get('background_tasks'),
#                                                name=cache_key,
#                                                value=func_result,
#                                                expiration_seconds=expiration)
#             else:
#                 logging.error(
#                     f'No background_tasks: BackgroundTasks in the controller arguments. Consider adding it to save the response of the controller after the response is sent to the user, making it faster.')
#                 await redis_client.set(name=cache_key,
#                                        value=func_result,
#                                        expiration_seconds=expiration)
#
#             return func_result
#
#         return wrapper
#
#     return actual_decorator
