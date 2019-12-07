@y.defer_constructor
def init_1():
    if y.config.get('psy'):
        y.run_at_exit(y.print_stats)


def select_handler(mode):
    name = 'cli_' + mode

    try:
        return eval('y.' + name + '.' + name)
    except AttributeError:
        pass
    
    return eval('y.' + name)


async def run_main(args):
    func0 = select_handler(args[1])
    
    y.prompt('/p1')

    return await func0(args[2:])
