def xcheck_file(pp, diff):
    y.xprint_green('checking ' + pp)

    with open(pp) as f:
        d = f.read()

    nd = y.preprocess_text(d, args={'OS': '"LINUX"', 'ARCH': '"X_86_64"', '__LINUX__': '1', 'X86_64': '1'})

    if nd != d:
        if diff:
            for l in y.difflib.unified_diff(nd, d, fromfile=pp, tofile=pp):
                y.xprint_red(l)
        else:
            y.xprint_magenta('-------------------------\n' + d)
            y.xprint_yellow('+++++++++++++++++++++++++++\n' + nd)
                


@y.main_entry_point
async def cli_dev_pdiff(args):
    for v in args:
        if y.os.path.isfile(v):
            xcheck_file(v, True)
        else:
            for a, b, c in y.os.walk(v):
                for x in c:
                    pp = y.os.path.join(a, x)
                    xcheck_file(pp, True)


@y.main_entry_point
async def cli_dev_preproc(args):
    for v in args:
        if y.os.path.isfile(v):
            xcheck_file(v, False)
        else:
            for a, b, c in y.os.walk(v):
                for x in c:
                    pp = y.os.path.join(a, x)
                    xcheck_file(pp, False)
