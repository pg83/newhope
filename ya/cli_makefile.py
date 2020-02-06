@y.main_entry_point
async def cli_dev_makefile(arg):
    parser = y.argparse.ArgumentParser()
   
    parser.add_argument('-o', '--output', default='', action='store', help='file to output, stdout by default')
    parser.add_argument('-P', '--plugins', default=[], action='append', help='where to find build rules')
    parser.add_argument('-O', '--os', default='', action='store', help='filter targets by os')

    args = parser.parse_args(arg)
    iter_cc = y.iter_tcs(args.os)

    with y.defer_context() as defer:
        if args.output:
            f = open(args.output, 'w')
            defer(f.close)
        else:
            f = y.stdout

        async def main_func():
            data = await y.main_makefile(iter_cc, y.all_distro_packs())

            def func():
                f.write(data)
                f.flush()

            return await y.offload(func)

        return await main_func()
