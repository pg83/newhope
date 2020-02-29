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
