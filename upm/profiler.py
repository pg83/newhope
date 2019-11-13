def profile(func, really=True):
    if not really:
        return func

    @y.functools.wraps(func)
    def wrapper(*args, **kwargs):
        p = y.cProfile.Profile()

        try:
            return p.runcall(func, *args, **kwargs)
        finally:
            ps = y.pstats.Stats(p, stream=y.sys.stderr)

            ps.sort_stats('cumtime')
            ps.print_stats()

    return wrapper
