@y.main_entry_point
async def cli_dev_debug(args):
    bdir = args[0]

    with open(bdir + '/run.sh', 'r') as f:
        data = f.read()

    with open(bdir + '/copy.sh', 'w') as f:
        f.write('trap "exec /bin/bash" exec')
        f.write(data)

    y.os.execv('/bin/bash', [bdir + '/copy.sh'])
