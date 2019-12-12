@y.main_entry_point
async def cli_pkg_make(arg):
    p = y.argparse.ArgumentParser()
    
    p.add_argument('-j', '--threads', default=1, action='store', help='set num threads')
    p.add_argument('-f', '--path', default='gen', action='store', help='path to Makefile, "-" - read from stdin, "gen" - generate on the fly')
    p.add_argument('-r', '--root', default=None, action='store', help='main root for build files')
    p.add_argument('-i', '--install-dir', default=None, action='store', help='where to install packages')
    p.add_argument('-d', '--do-not-remove', default=None, action='store', help='не удалять даннные')
    p.add_argument('-s', '--shell', default=None, action='store', help='указать шелл для сборки')
    p.add_argument('--production', default=False, action='store_const', const=True, help='production execution')
    p.add_argument('--curses', default=False, action='store_const', const=True, help='use curses gui')
    p.add_argument('--proxy', default=False, action='store_const', const=True, help='serve as as a stream proxy')
    p.add_argument('targets', nargs=y.argparse.REMAINDER)

    args = p.parse_args(arg)
    local = not args.production

    if local and args.install_dir:
        raise Exception('do not do this, kids, at home')

    def calc_root():
        if args.root:
            return args.root

        if local:
            return y.upm_root()

        if args.production:
            return '/d'

        raise Exception('can not determine root')

    root = calc_root()

    def iter_replaces():
        if args.install_dir:
            yield ('$PD', args.install_dir)

        yield ('$MD', '$PREFIX/m')
        yield ('$RD', '$PREFIX/r')
        yield ('$WD', '$PREFIX/w')
        yield ('$SD', '$PREFIX/s')

        if local:
            yield ('$PD', '$PREFIX/p')

        if args.production:
            yield ('$PD', '/private')

        yield ('$PREFIX', root)
        yield ('$UPM', y.globals.script_path)

        if args.shell:
            yield ('$YSHELL', args.shell)

    shell_vars = dict(iter_replaces())
    
    async def gen():
        mk, portion = await y.main_makefile(y.iter_cc, internal=True)
        
        return y.loads_mk(mk)

    mk = await y.open_mk_file(args.path, gen)
    
    if int(args.threads):
        args.pre_run = ['workspace']
        args.shell_vars = shell_vars
        
        return await mk.build(args)

    return 0
