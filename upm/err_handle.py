def abort_on_error(func):
    @y.functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            try:
                y.stderr.out(func.__module__, func.__name__)
                y.print_all_stacks()
            finally:
                y.os.abort()
            
    return wrapper


def stop_iter(*args, **kwargs):
    raise StopIteration()


def run_down_once():
    @y.singleton
    def run_down_once_impl():
        y.broadcast_channel('SIGNAL')({'signal': 'DOWN', 'when': 'now'})

    run_down_once_impl()
