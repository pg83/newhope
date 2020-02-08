ENTRY = [
    'exec unshare --fork --pid --kill-child /usr/bin/timeout 4h /media/build/upm cmd scheduler BUILD'
]

BUILD = [
    ['cd /tmp && echo "start cycle" && /home/pg83/newhope/cli release > upm && chmod +x upm && ./upm && mv ./upm /media/build && echo "done cycle" && sleep 8'],
    ['echo | tr -d "\n"'],
    ['/media/build/upm pkg sync repo --fr /home/pg83/upm_root/r --fr /media/build/r --to /media/storage && sleep 5'],
    ['/usr/bin/timeout 10m /media/build/upm pkg serve repo --fr /media/storage'],
    ['cd /media/build && ./upm makefile --os linux -v | ./upm make --root /media/build --install-dir /pkg -j5 -f -']
]


def func(code):
    def do():
        while True:
            try:
                y.info('will run', code)
                y.subprocess.Popen(code, shell=True).communicate(input='')
                y.info('done')
            except Exception as e:
                y.warning('in scheduler:', e)

            y.time.sleep(1)

    return do


@y.main_entry_point
async def cli_cmd_scheduler(args):
    code = (len(args) > 0 and args[0]) or 'ENTRY'

    y.info('code', code)

    thrs = [y.threading.Thread(target=func(c)) for c in globals()[code]]

    for t in thrs:
        t.start()

    for t in thrs:
        t.join()

