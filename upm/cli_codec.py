@y.main_entry_point
async def cli_codec(args):
    f = y.sys.stdout
    d = y.sys.stdin.buffer.read()
    
    if args[0] == '-c':
        f.buffer.write(y.lzma.compress(d))
    else:
        f.buffer.write(y.lzma.decompress(d))

    f.buffer.flush()
    f.flush()
