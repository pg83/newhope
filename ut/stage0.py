def run_stage0(g):
    def iter_modules():
        yield 'ut/iface.py'
        yield 'ut/mod_load.py'
        yield 'ut/stage1.py'

    def iter_data():
        for i in iter_modules():
            yield g.by_name[i]['data']

        yield '\nrun_stage1(_globals)\n'

    ctx = {'_globals': g}
    exec(g.compile('\n'.join(iter_data()), '0:stage1.py', 'exec'), ctx)
    ctx.clear()
