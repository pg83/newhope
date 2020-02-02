@y.main_entry_point
async def cli_dev_debug(args):
    bdir = args[0] + '/runtime'

    if not y.os.path.isfile(bdir + '/copy.sh'):
        with open(bdir + '/run.sh', 'r') as f:
            data = f.read()

        with open(bdir + '/copy.sh', 'w') as f:
            f.write('trap "exec /bin/bash" exit\n')
            f.write(data)

    y.os.chdir(args[0])
    y.os.execv('/bin/bash', ['/bin/bash', bdir + '/copy.sh'])
