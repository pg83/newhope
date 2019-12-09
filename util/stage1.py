import sys


def create_main(g):
    sys.modules['ya'] = -1
    sys.modules['gn'] = -1
    sys.modules['pl'] = -1
    sys.modules['ut'] = -1

    def re_exec(g):
        code = """
def new_main(loader, g):
    builtin = dict((x['name'].replace('/', '.')[:-3], x) for x in g.file_data)
    mod = loader(builtin).create_module('ut.mod_load')
    g.builtin_modules = builtin
    mod.bootstrap(mod, g)

new_main(loader, _globals)
"""
        ctx = {'loader': Loader, '_globals': g}
        exec(compile(code, '2:stage1.py', 'exec'), ctx)
        ctx.clear()

    return re_exec


def run_stage1(g):
    ctx = {'re_exec': create_main(g), '_globals': g}
    exec(compile('re_exec(_globals)', '1:stage1.py', 'exec'), ctx)
    ctx.clear()
