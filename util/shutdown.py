def get_white_line():
    return '{w}-----------------------------------------------{}'


def kill_all_running(*args):
    running_os = 'linux' #y.platform.system().lower()

    if running_os == 'darwin':
        return y.os.system('pkill -KILL -g {pgid}'.format(pgid=y.os.getpgid(y.os.getpid())))

    if running_os == 'linux':
        return y.os.system('pkill -KILL -P {ppid}'.format(ppid=y.os.getpid()))

    raise Exception('todo')


def run_sigint(*args):
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
