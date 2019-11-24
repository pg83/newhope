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
    return y.DEFER_LOOP.write_channel('DEFERC', 'common')
    

def defer_constructor(func):
    defer_channel()({'func': func})
    
    return func


def run_defer_constructors():
    @defer_constructor
    def init_log():
        if '/debug' in y.verbose:
            y.logging.basicConfig(level='DEBUG')
        
    @defer_constructor
    def sentinel():
        return 'shit'

    defer_callback = defer_channel().read_callback()

    @defer_callback
    def on_defer_constructor(arg):
        if str(arg['func']()) == 'shit':
            raise y.StopNow()

    y.DEFER_LOOP.run_loop()
