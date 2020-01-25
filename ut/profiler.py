def run_profile(func, really=False):
    if not really:
        return func

    @y.functools.wraps(func)
    def wrapper(*args, **kwargs):
        p = y.cProfile.Profile()

        try:
            return p.runcall(func, *args, **kwargs)
        finally:
            @y.run_at_exit
            @y.singleton
            def func():
                ps = y.pstats.Stats(p, stream=y.stderr)

                ps.sort_stats('cumtime')
                ps.print_stats()

            func()

    return wrapper
