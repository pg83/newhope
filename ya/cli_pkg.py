@y.main_entry_point
async def cli_pkg_add(args):
    pass


@y.main_entry_point
async def cli_pkg_sync_repo(args_):
    parser = y.argparse.ArgumentParser()

    parser.add_argument('--fr', default=[], action='append', help='input repo')
    parser.add_argument('--to', default='', action='store', help='output repo')

    args = parser.parse_args(args_)

    assert args.fr
    assert args.to

    try:
        y.os.makedirs(args.to)
    except OSError:
        pass

    while True:
        for fr in args.fr:
            for x in y.os.listdir(fr):
                z = y.os.path.join(args.to, x)

                if y.os.path.isfile(z):
                    y.info('already exists', z)
                else:
                    y.info('copy file ', x, ' to ', z)
                    y.shutil.copyfile(y.os.path.join(fr, x), z + '.tmp')
                    y.os.rename(z + '.tmp', z)

            
        index = []

        y.info('will write index')

        for f in sorted(y.os.listdir(args.to)):
            if len(f) > 10:
                p = y.os.path.join(args.to, f)
        
                if f.endswith('-tmp'):
                    y.os.unlink(p)
                    continue

                index.append({'path': f, 'length': y.os.path.getsize(p), 'ts': int(1000000 * y.os.path.getmtime(p))})
        
        with open(args.to + '/index', 'w') as f:
            f.buffer.write(y.encode_prof(index))


@y.main_entry_point
async def cli_pkg_serve(args):
    pass
