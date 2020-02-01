import os

@y.main_entry_point
async def cli_cmd_codec(args):
    with y.without_color():
        so = y.sys.stdout
        si = y.sys.stdin

        if args[0] == '-c':
            so.buffer.write(y.encode_prof(si.buffer.read()))
        elif args[0] == '-d':
            so.buffer.write(y.decode_prof(si.buffer.read()))
        else:
            raise Exception('shit')

        so.flush()

