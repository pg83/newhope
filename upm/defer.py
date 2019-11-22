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
    return y.MAIN_LOOP.write_channel('DEFERC', 'common')
    

def defer_constructor(func):
    defer_channel()({'func': func})
    
    return func


@y.abort_on_error
def run_defer_constructors():
    @defer_constructor
    def sentinel():
        return 'shit'
    
    rq, wq = y.MAIN_LOOP.subscribe_queue('DEFERC', 'main')

    while True:
        for f in rq():
            if '/show_defer' in y.verbose:
                y.xprint_dg('run constructor', f)

            res = str(f['func']())
            
            if res == 'shit':
                return
