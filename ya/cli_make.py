@y.main_entry_point
def cli_dev_make(arg):
    p = y.argparse.ArgumentParser()

    p.add_argument('-j', '--threads', default=1, action='store', help='set num threads')
    p.add_argument('-f', '--path', default='gen', action='store', help='path to Makefile, "-" - read from stdin, "gen" - generate on the fly')
    p.add_argument('-r', '--root', default=None, action='store', help='main root for build files')
    p.add_argument('-i', '--install-dir', default=None, action='store', help='where to install packages')
    p.add_argument('-s', '--shell', default=None, action='store', help='указать шелл для сборки')
    p.add_argument('-k', '--keep-going', default=False, action='store_const', const=True, help='продолжать сборку после ошибок')
    p.add_argument('--naked', default=False, action='store_const', const=True, help='show command output as is')
    p.add_argument('targets', nargs=y.argparse.REMAINDER)

    args = p.parse_args(arg)

    def calc_root():
        if args.root:
            return args.root

        with y.open_pdb() as db:
            if 'build_prefix' in db.kv:
                return db.kv['build_prefix']

        return y.upm_root()

    root = calc_root()

    def iter_replaces():
        if args.install_dir:
            yield ('$PD', args.install_dir)

        yield ('$MD', '$PREFIX/m')
        yield ('$RD', '$PREFIX/r')
        yield ('$WD', '$PREFIX/w')
        yield ('$SD', '$PREFIX/s')

        if args.install_dir:
            yield ('$PD', args.install_dir)
        else:
            yield ('$PD', '$PREFIX/p')
        
        yield ('$PREFIX', root)
        yield ('$UPM', y.globals.script_path)

        if args.shell:
            yield ('$YSHELL', args.shell)

    shell_vars = dict(iter_replaces())

    def gen():
        return y.main_makefile(y.iter_all_cc, True, kind='data')

    mk = y.open_mk_file(args.path, gen)

    if int(args.threads):
        if not args.targets:
            args.targets = ['all']

        args.pre_run = ['workspace']
        args.shell_vars = shell_vars

        return mk.build(args)

    return 0
