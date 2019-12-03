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


@y.contextlib.contextmanager
def abort_on_error():
    try:
        yield
    finally:
        if not y.exc_info()[0]:
            y.print_all_stacks()
            y.os.abort()


def stop_iter(*args, **kwargs):
    raise y.StopNow()


async def async_stop_iter(*args, **kwargs):
    raise y.StopNow()

    
def on_except():
    try:
        y.debug(y.traceback.format_exc())
    finally:
        y.os.abort()


def safe_run(f):
    try:
        return f()
    except Exception:
        on_except()


def sync_pack(f):
    try:
        return ([f()], None)
    except Exception:
        return (None, y.sys.exc_info())

    
async def async_pack(f):
    try:
        res = await f()
        
        return ([res], None)
    except Exception:
        return (None, y.sys.exc_info())


def unpack(r):
    res, exc = r

    if res:
        return res[0]

    raise exc[0](exc[1]).with_traceback(exc[2])    


def print_stacks():
    while True:
        y.time.sleep(5)
        y.print_all_stacks()

        
#y.threading.Thread(target=print_stacks).start()
