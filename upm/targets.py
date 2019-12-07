import os
import sys


async def gen_packs(constraints=None):
    constraints = constraints or y.get_all_constraints

    def iter():
        for func in y.gen_all_funcs():
            for c in constraints():
                yield func(y.deep_copy(c))

    return list(iter())
