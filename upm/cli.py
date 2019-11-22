@y.defer_constructor
def init_1():
    if '/psy' in y.verbose:
        y.atexit.register(y.print_stats)
        

def select_handler(mode):
    name = 'cli_' + mode

    try:
        return eval('y.' + name + '.' + name)
    except AttributeError:
        pass
    
    return eval('y.' + name)


def run_main(args):
    func1 = select_handler(args[1])
    func2 = lambda: func1(args[2:])
    func3 = y.run_profile(func2, really=y.need_profile)

    y.prompt('/p1')

    try:
        func3()
    finally:
        y.run_down_once()
