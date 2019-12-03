@y.singleton
def at_exit():
    ae = y.collections.deque()

    return ae


def run_at_exit(f):
    at_exit().append(f)

    return f


def run_handlers():
    try:
        while True:
            f = at_exit().pop()
            y.debug('run', f.__module__ + '.' + f.__name__)
            f()
    except IndexError:
        pass
