def run_cc_profile(func):
    f = func

    def wrapper(*args, **kwargs):
        p = y.profile.Profile()

        try:
            return p.runcall(f, *args, **kwargs)
        finally:
            @y.run_at_exit
            @y.singleton
            def func():
                ps = y.pstats.Stats(p, stream=y.stderr)

                ps.sort_stats('cumtime')
                ps.print_stats()

            func()

    return wrapper
