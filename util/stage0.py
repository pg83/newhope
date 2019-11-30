def run_stage0(args, data, by_name, **kwargs):
    def iter_modules():
        yield 'ut/iface.py'
        yield 'ut/init_log.py'
        yield 'ut/args_parse.py'
        yield 'ut/mod_load.py'
        yield 'ut/stage1.py'

    def iter_data():
        for i in iter_modules():
            yield by_name[i]['data']

        yield '\nrun_stage1(args, **args)\n'

    ctx = {'args': args}
    exec(compile('\n'.join(iter_data()), '0:stage1.py', 'exec'), ctx)
    ctx.clear()
