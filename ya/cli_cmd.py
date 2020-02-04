@y.main_entry_point
async def cli_cmd_subst(args):
    assert len(args) == 3

    path = args[0]
    
    with open(path, 'r') as f:
        data = f.read()

    y.write_file(path, data.replace(args[1], args[2]).encode('utf-8'))
