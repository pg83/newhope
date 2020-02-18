def func(code_):
    def do():
        code = code_

        while True:
            try:
                y.info('will run', code)

                p = y.subprocess.Popen(code, shell=True)
                retcode = p.wait()

                y.info('done, with code', retcode)
            except Exception as e:
                y.warning('in scheduler:', y.traceback.format_exc())

            y.time.sleep(1)

    return do


def wait_pid():
    while True:
        try:
            for i in range(0, 10):
                y.info('got something', y.os.waitpid(0, y.os.WNOHANG))
        except Exception as e:
            y.warning('in process catch: s', e)

        y.time.sleep(1)


def watch_dog():
    y.time.sleep(4 * 3600)
    y.shut_down(retcode=11, last_msg='watchdog happen')


def gen_wd_func(f):
    try:
        f.__name__

        y.info('will run', f.__name__)

        return f
    except AttributeError:
        y.info('will run', f)

        return func(f)


def exec_build():
    y.os.execl('/usr/bin/unshare', 'unshare', '--fork', '--pid', '--kill-child', '/media/build/upm', 'cmd', 'scheduler', 'BUILD')


ENTRY = [
    exec_build,
]


BUILD = [
    ['cd /tmp && echo "start cycle" && /home/pg83/newhope/cli release > upm && chmod +x upm && ./upm && mv ./upm /media/build && echo "done cycle" && sleep 8'],
    ['echo | tr -d "\n"'],
    ['/media/build/upm pkg sync repo --fr /media/build/r --to /media/storage && sleep 5'],
    ['/usr/bin/timeout 10m /media/build/upm pkg serve repo --fr /media/storage --port 10000'],
    ['cd /media/build && ./upm makefile --os linux -v | ./upm make --keep-going --root /media/build --install-dir /pkg -j7 -f-'],
    ['cd /media/storage && (find . | grep "\-tmp" | xargs rm) && sleep 1200'],
    wait_pid,
    watch_dog,
]


CRON = [
    ['sleep 10'],
]


@y.verbose_entry_point
def cli_cmd_scheduler(args):
    y.os.nice(20)
    code = (len(args) > 0 and args[0]) or 'ENTRY'
    y.info('code', code)
    thrs = [y.threading.Thread(target=gen_wd_func(c)) for c in globals()[code]]

    for t in thrs:
        t.start()

    for t in thrs:
        t.join()
