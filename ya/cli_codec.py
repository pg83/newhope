@y.contextlib.contextmanager
def switch_stdout():
    cur = y.sys.stdout
    prev = cur.slave()

    y.sys.stdout = prev

    try:
        yield prev
    finally:
        y.sys.stdout = cur


@y.main_entry_point
async def cli_cmd_codec(args):
    with switch_stdout() as f:
        d = y.sys.stdin.buffer.read()

        if args[0] == '-c':
            f.buffer.write(y.lzma.compress(d))
        elif args[0] == '-d':
            f.buffer.write(y.lzma.decompress(d))
        else:
            raise Exception('shit')

        f.flush()
