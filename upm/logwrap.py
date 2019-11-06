import functools
import traceback


def logged_wrapper(rethrow=None, tb=False, rfunc=None, important=False):
    def decorator(func):
        if not important:
            return func 

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if tb:
                    y.xprint_red(traceback.format_exc(e), *args, **kwargs)
                else:
                    print func, args, kwargs, e

                if rethrow is None:
                    raise

            return rethrow

        wrapper.__name__ = func.__name__

        return wrapper

    if rfunc:
        return decorator(rfunc)

    return decorator
