def kill_all_running(*args):
    y.os.system('pkill -KILL -g {pgid}'.format(pgid=y.os.getpgid(y.os.getpid())))


def run_sigint(*args):
    y.run_handlers()
    y.last_msg(y.process_color('\r' + y.get_white_line() + '\n{r}build failed{}\n', '', {}))
    y.os._exit(8)


def shut_down():
    y.time.sleep(3)
    y.run_handlers()
    kill_all_running()
    kill_all_running()
    y.os._exit(10)
    
    
@y.defer_constructor
def init_shutdown():
    y.sys.modules['__main__'].real_handler = run_sigint
