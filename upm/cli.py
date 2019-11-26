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
    func0 = select_handler(args[1])
    func1 = lambda: func0(args[2:])
    func2 = y.run_profile(func1, really=('/profile' in y.verbose))

    y.prompt('/p1')

    try:
        return func2()
    finally:
        y.run_down_once()
