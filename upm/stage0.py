def run_stage0(args, data, by_name, **kwargs):
    def iter_modules():
        yield 'ya/iface.py'
        yield 'ya/init_log.py'
        yield 'ya/args_parse.py'
        yield 'ya/mod_load.py'
        yield 'ya/stage1.py'

    def iter_data():
        for i in iter_modules():
            yield by_name[i]['data']

        yield '\nrun_stage1(args, **args)\n'

    ctx = {'args': args}
    exec(compile('\n'.join(iter_data()), '0:stage1.py', 'exec'), ctx)
    ctx.clear()
