@y.main_entry_point
async def cli_cmd_pgmake(args):
    p = y.argparse.ArgumentParser()

    p.add_argument('-j', '--threads', default=1, action='store', help='set num threads')
    p.add_argument('-f', '--path', default='', action='store', help='path to Makefile, "-" - read from stdin')
    p.add_argument('-s', '--set', default=[], action='append', help='set shell variable for makefile')
    p.add_argument('targets', nargs=y.argparse.REMAINDER)

    args = p.parse_args(args)
    mk = await y.open_mk_file(args.path)

    def iter_vars():
        for i in args.set:
            k, v = i.split('=')

            yield '$' + k, v

    await mk.build_kw(shell_vars=dict(iter_vars()), threads=args.threads, targets=args.targets, pre_run=[])
