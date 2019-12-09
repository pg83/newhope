def run_stage2(g):
    args, verbose, profile = y.parse_args(y.sys.argv)

    def iter_cfg():
        for v in verbose.split(','):
            parts = v.split('=')

            if len(parts) >= 2:
                yield parts[0], parts[1]

            if len(parts) == 1:
                yield parts[0], True

    config = dict(iter_cfg())

    def run_thr():
        fd = {
            'verbose': verbose,
            'need_profile': profile,
            'args': args,
            'config': config,
            'globals': g,
        }

        y.Loader(g.builtin_modules).create_module('ut.iface').run_stage4_0(fd)

    t = y.threading.Thread(target=run_thr)
    t.start()
