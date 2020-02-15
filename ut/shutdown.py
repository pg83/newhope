def get_white_line():
    return '{w}-----------------------------------------------{}'


def kill_all_running(*args):
    y.os.killpg(y.os.getpgid(y.os.getpid()), y.signal.SIGTERM)


def run_sigint(*args):
    y.stderr.set_sb_cb(None)
    y.stderr.write('\r\n')
    y.stderr.flush()
    last_msg = get_white_line() + '\n{br}system failure{}\n'
    shut_down(retcode=8, last_msg=last_msg)


def shut_down(retcode=10, last_msg=''):
    y.run_handlers()
    kill_all_running()
    y.last_msg(last_msg)
    y.os._exit(retcode)


@y.defer_constructor
def init_shutdown():
    y.globals.sigint_handler = run_sigint
