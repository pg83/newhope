@y.verbose_entry_point
def cli_cmd_subst(args):
    if len(args) == 2:
        with open(args[1]) as f:
            data = f.read()

        a, b = data.split('\n', 1)

        a = a.strip()[2:]
        b = b.strip()[2:]
    else:
        a = args[1]
        b = args[2]

    path = args[0]

    with open(path, 'r') as f:
        data = f.read()

    y.write_file(path, data.replace(a, b), mode='w')


@y.verbose_entry_point
def cli_cmd_rmtmp(args):
    for d in args:
        d = y.os.path.abspath(d)

        for x in y.os.listdir(d):
            p = y.os.path.join(d, x)

            if y.is_tmp_name(p):
                y.info('remove stale', p)

                try:
                    y.os.unlink(p)
                except Exception as e:
                    y.info('in remove stale', p, e)

                    try:
                        y.shutil.rmtree(p)
                    except Exception as e:
                        y.info('in remove stale', p, e)

