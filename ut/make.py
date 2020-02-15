class OutputResult(object):
    def __init__(self, status_bar):
        self._in_fly = set()
        self._sb = status_bar
        self._complete = 0
        self._st = y.time.time()

    def set_sb(self):
        self._sb.set_data(self.render())

    def output_build_results(self, arg):
        if 'target' in arg:
            tg = y.to_pretty_name(arg.pop('target'))
            arg['_target'] = tg
            msg = arg.get('message', '')

            if 'starting' in msg:
                self._in_fly.add(tg)
                self.set_sb()
            else:
                try:
                    self._in_fly.remove(tg)
                    self._complete += 1
                    self.set_sb()
                except Exception:
                    pass

        if 'output' in arg:
            data = arg.pop('output').strip()

        if (status := arg.get('status', '')) == 'fail':
            arg['message'] = arg.get('message', '') + '\n' + data

        if 'message' in arg:
            y.build_results({'info': {'message': arg.pop('message'), 'extra': arg}})

        if 'info' in arg:
            y.info(arg['info']['message'], extra=arg['info']['extra'])

    def render(self):
        cols = self._sb.get_columns()
        in_fly = sorted(list(self._in_fly))

        def get_part(x):
            try:
                return x.split('-')[1]
            except Exception:
                return x

        in_fly = [get_part(x) for x in in_fly]

        b = y.get_color_ext(None, 'on_grey', attrs=['light', 'reverse'])
        e = y.get_code(0)

        return b + ('complete: ' + str(self._complete) + ', run time: ' + str(int(y.time.time() - self._st)) + ', in fly: ' + ', '.join(in_fly) + ' ' * 200)[:cols] + e


def run_make_0(mk, args):
    #if args.naked:
    #    return run_make_1(mk, args, y.FakeStatusBar())

    with y.with_status_bar(y.sys.stderr) as status_bar:
        return run_make_1(mk, args, status_bar)


def run_make_1(mk, args, status_bar):
    ores = OutputResult(status_bar)

    @y.lookup
    def lookup(name):
        return {'build_results': ores.output_build_results}[name]

    return y.run_makefile(mk, args.targets, int(args.threads), pre_run=args.pre_run, naked=args.naked)
