def abort_on_error(func):
    @y.functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except y.StopNow:
            raise
        except StopIteration:
            raise
        except Exception:
            try:
                y.debug(func.__module__, func.__name__)
                y.print_tbx()
            finally:
                y.os.abort()
            
    return wrapper


def stop_iter(*args, **kwargs):
    raise y.StopNow()


async def async_stop_iter(*args, **kwargs):
    raise y.StopNow()


@y.singleton
def run_down_once():
    y.broadcast_channel('SIGNAL')({'signal': 'DOWN', 'when': 'now'})
