@y.contextlib.contextmanager
def without_gc(print_stats=False):
    ygc = y.gc

    try:
        ygc.disable()
        yield ygc
    finally:
        ygc.enable()
        
        if print_stats:
            y.xprint_r(ygc.garbage)
