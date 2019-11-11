def logged_wrapper(rethrow=None, rfunc=None, important=False):
    def decorator(func):
        if not important:
            return func 
        
        @y.functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                y.print_tbx()

                if rethrow is None:
                    raise e

            return rethrow

        wrapper.__name__ = func.__name__

        return wrapper

    if rfunc:
        return decorator(rfunc)

    return decorator
