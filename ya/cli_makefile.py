def iter_all_cc():   
    for t in y.iter_all_targets():
        yield y.dc(t)


@y.main_entry_point
async def cli_pkg_makefile(arg):
    parser = y.argparse.ArgumentParser()
   
    parser.add_argument('-o', '--output', default='', action='store', help='file to output, stdout by default')
    parser.add_argument('-S', '--shell', default=[], action='append', help='out build.sh script')
    parser.add_argument('-P', '--plugins', default=[], action='append', help='where to find build rules')
    parser.add_argument('-I', '--internal', default=False, action='store_const', const=True, help='generte internal format')
    parser.add_argument('-T', '--dot', default=False, action='store_const', const=True, help='output dot graph')
    parser.add_argument('-F', '--dump', default=False, action='store_const', const=True, help='output full dump')
    parser.add_argument('-O', '--os', default='', action='store', help='filter targets by os')

    args = parser.parse_args(arg)

    if args.os:
        def iter_cc():
            for t in iter_all_cc():
                if t['os'] == args.os:
                    yield y.dc(t)
    else:
        iter_cc = iter_all_cc

    with y.defer_context() as defer:
        if args.output:
            f = open(args.output, 'w')
            defer(f.close)
        else:
            f = y.stdout

        async def main_func():
            if args.dot:
                data = print(await y.build_dot_script(iter_cc))
            elif args.shell:
                data = await y.build_sh_script(args.shell)
            elif args.dump:
                data = await y.gen_full_dump(iter_cc)
            else:
                data = await y.main_makefile(iter_cc, internal=args.internal)

                def func():
                    f.write(data)
                    f.flush()

                return await y.offload(func)

        return await main_func()
