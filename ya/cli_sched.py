def proc_func(code_):
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
                y.debug('got something', y.os.waitpid(0, y.os.WNOHANG))
        except Exception as e:
            y.warning('in process catch: s', e)

        y.time.sleep(1)


def watch_dog():
    y.time.sleep(4 * 3600)
    y.shut_down(retcode=11, last_msg='watchdog happen')


def exec_build():
    y.os.execl('/usr/bin/unshare', 'unshare', '--fork', '--pid', '--kill-child', '/media/build/upm', 'cmd', 'scheduler', 'BUILD')


ENTRY = [
    exec_build,
]


BUILD_PROC = [
    ['((rm -rf /media/build/t || true) 2> /dev/null) && mkdir /media/build/t && cd /media/build/t && git clone https://github.com/pg83/newhope.git && ./newhope/cli release > upm && chmod +x upm && ./upm && mv ./upm /media/build && sleep 120'],
    ['/media/build/upm pkg sync repo --fr /media/build/r --to /media/storage && sleep 30'],
    ['/media/build/upm cmd rmtmp /media/build/r && sleep 120'],
    ['/media/build/upm cmd rmtmp /media/storage && sleep 120'],
    ['/usr/bin/timeout 30m /media/build/upm pkg serve repo --fr /media/storage --port 10000'],
    ['cd /media/build && (./upm makefile --os linux -v | ./upm make --keep-going --root /media/build --install-dir /pkg -j10 -f- -v)'],
]


BUILD = [
    wait_pid,
    watch_dog,
] + [proc_func(x) for x in BUILD_PROC]


@y.verbose_entry_point
def cli_cmd_scheduler(args):
    y.os.nice(20)

    code = (len(args) > 0 and args[0]) or 'ENTRY'
    y.info('code', code)

    thrs = [y.threading.Thread(target=c) for c in y.find(code)]

    for t in thrs:
        t.start()

    for t in thrs:
        t.join()
