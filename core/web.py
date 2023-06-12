from functools import wraps


def sensitive_fields(fields: list):
    def sensitive_fields_decorator(func):
        @wraps(func)
        async def _wrapper(*args, **kwargs):
            response = await func(*args, **kwargs)
            for field in fields:
                if hasattr(response, field):
                    delattr(response, field)
            return response

        return _wrapper

    return sensitive_fields_decorator
