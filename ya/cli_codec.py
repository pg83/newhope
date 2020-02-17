import os


@y.verbose_entry_point
def cli_cmd_codec(args):
    so = y.sys.__stdout__
    si = y.sys.__stdin__

    if args[0] == '-c':
        so.buffer.write(y.encode_prof(si.buffer.read()))
    elif args[0] == '-d':
        so.buffer.write(y.decode_prof(si.buffer.read()))
    else:
        raise Exception('shit')

    so.flush()
    y.os._exit(0)

