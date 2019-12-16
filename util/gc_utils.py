@y.contextlib.contextmanager
def without_gc(print_stats=False):
    ygc = y.gc

    try:
        ygc.disable()
        
        yield ygc
    finally:
        ygc.enable()
        
        if print_stats:
            if ygc.garbage:
                y.xprint_r('gc garbage left:', ygc.garbage)
