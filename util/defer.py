y.pubsub

@y.contextlib.contextmanager
def defer_context(verbose=False):
    defer = []
    
    try:
        yield defer.append
    finally:
        for d in defer:
            try:
                d()
            except Exception:
                pass
        

def defer_wrapper(func):
    @y.functools.wraps(func)
    def wrapper(*args, **kwargs):
        with defer_context(verbose=True) as defer:
            return func(defer, *args, **kwargs)

    return wrapper


@y.singleton
def defer_channel():
    return []
    

def defer_constructor(func):
    defer_channel().append({'func': func})
    
    return func


def run_defer_constructors():
    @defer_constructor
    def init_log():
        if '/debug/loglevel' in y.verbose:
            y.logging.basicConfig(level='DEBUG')
        
    @defer_constructor
    def sentinel():
        return 'shit'

    while True:
        for arg in defer_channel():
            res = str(arg['func']())

            if res == 'shit':
                return
