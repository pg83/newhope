def kill_all_running(*args):
    #y.os.system('pkill -KILL -g {pgid}'.format(pgid=y.os.getpgid(y.os.getpid())))
    y.os.system('pkill -KILL -P {ppid}'.format(ppid=y.os.getpid()))


def run_sigint(*args):
    y.stderr.write('\r\n')
    y.run_handlers()
    y.last_msg(y.get_white_line() + '\n{br}system failure{}\n')
    y.os._exit(8)


def shut_down(retcode=10):
    y.run_handlers()
    kill_all_running()
    kill_all_running()
    y.last_msg('')
    y.os._exit(retcode)


@y.defer_constructor
def init_shutdown():
    y.sys.modules['__main__'].real_handler = run_sigint
