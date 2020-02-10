@y.main_entry_point
def cli_dev_makefile(arg):
    parser = y.argparse.ArgumentParser()
   
    parser.add_argument('-o', '--output', default='', action='store', help='file to output, stdout by default')
    parser.add_argument('-P', '--plugins', default=[], action='append', help='where to find build rules')
    parser.add_argument('-O', '--os', default='', action='store', help='filter targets by os')
    parser.add_argument('-F', '--flat', default=False, action='store_const', const=True, help='build flat tree')

    args = parser.parse_args(arg)
    iter_cc = y.iter_tcs(args.os)

    with y.defer_context() as defer:
        if args.output:
            f = open(args.output, 'w')
            defer(f.close)
        else:
            f = y.stdout

        data = y.main_makefile(iter_cc, y.all_distro_packs(), args.flat)

        f.write(data)
        f.flush()
