@y.contextlib.contextmanager
def defer_context(verbose=False):
    defer = []
    xxf = y.xxformat

    try:
        yield defer.append
    finally:
        outs = []

        for d in defer:
            if d.__name__ != '<lambda>':
                outs.append(xxf(d.__name__.replace('_', ' '), init='white'))

            try:
                res = d()
                    
                if res:
                    outs.append(str(res))
            except Exception as e:
                outs.append(xxf('in defer:', y.traceback.format_exc(e), init='red'))
        
        if verbose:
            y.sys.stderr.write('\n'.join(outs) + '\n')
        

def defer_wrapper(func):
    @y.functools.wraps(func)
    def wrapper(*args, **kwargs):
        with defer_context(verbose=True) as defer:
            return func(defer, *args, **kwargs)

    return wrapper
