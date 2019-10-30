import sys
import cProfile
import pstats
import functools


def profile(func, really=True):
    if not really:
        return func

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        p = cProfile.Profile()

        try:
            return p.runcall(func, *args, **kwargs)
        finally:
            ps = pstats.Stats(p, stream=sys.stderr)

            ps.sort_stats('cumtime')
            ps.print_stats()

    return wrapper
