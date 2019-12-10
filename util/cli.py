@y.defer_constructor
def init_1():
    if y.config.get('psy'):
        y.run_at_exit(y.print_stats)
    

async def run_main(args):
    return await y.get_entry_point(args[1])(args[2:])
