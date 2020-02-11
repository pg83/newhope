ENTRY = [
    'exec nice -n 20 unshare --fork --pid --kill-child /media/build/upm cmd scheduler BUILD'
]

BUILD = [
    ['cd /tmp && echo "start cycle" && /home/pg83/newhope/cli release > upm && chmod +x upm && ./upm && mv ./upm /media/build && echo "done cycle" && sleep 8'],
    ['echo | tr -d "\n"'],
    ['/media/build/upm pkg sync repo --fr /home/pg83/upm_root/r --fr /media/build/r --to /media/storage && sleep 5'],
    ['/usr/bin/timeout 10m /media/build/upm pkg serve repo --fr /media/storage'],
    ['cd /media/build && ./upm makefile --os linux -v | ./upm make --root /media/build --install-dir /pkg -j5 -f -'],
    ['cd /media/storage && (find . | grep "\-tmp" | xargs rm) && sleep 1200']
]


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


def wp():
    while True:
        try:
            for i in range(0, 10):
                y.info('got something', y.os.waitpid(0, y.os.WNOHANG))
        except Exception as e:
            y.warning('in process catch: s', e)

        y.time.sleep(1)


@y.verbose_entry_point
def cli_cmd_scheduler(args):
    y.signal.alarm(4 * 3600)

    code = (len(args) > 0 and args[0]) or 'ENTRY'

    y.info('code', code)

    thrs = [y.threading.Thread(target=func(c)) for c in globals()[code]]  + [y.threading.Thread(target=wp)]

    for t in thrs:
        t.start()

    for t in thrs:
        t.join()
