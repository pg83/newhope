@y.main_entry_point
async def cli_cmd_subst(args):
    assert len(args) == 3

    with open(args[0], 'r') as f:
        data = f.read()

    data = data.replace(args[1], args[2])

    with open(args[0] + '.tmp', 'w') as f:
        f.write(data)

    y.os.rename(args[0] + '.tmp', args[0])
