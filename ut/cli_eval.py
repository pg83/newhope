@y.main_entry_point
def cli_dev_eval(args):
    run_eval(args)


def run_eval(args):
    repl = {}

    if not args:
        for k, v in repl.items():
            y.xprint_bb(k, '=', v)

        return

    for a in args:
        try:
            print(eval(repl.get(a, a)))
        except:
            y.print_tbx(tb_line='can not run ' + a)


@y.main_entry_point
def cli_dev_repl(args):
    y.run_repl()
