ENTRY = [
    'unshare --fork --pid --mount-proc --kill-child /usr/bin/timeout 4h /media/build/repo/upm cmd scheduler BUILD'
]

BUILD = [
    ['cd /tmp && echo "start cycle" && /root/newhope/cli release > upm && chmod +x upm && ./upm && mv ./upm /media/build/repo && echo "done cycle" && sleep 8'],
    ['echo | tr -d "\n"'],
    ['/media/build/repo/upm pkg sync repo --fr /media/build/dev/r --to /media/storage/pkg_repo && sleep 5'],
    ['/usr/bin/timeout 10m /media/build/repo/upm pkg serve repo --fr /media/storage/pkg_repo'],
    ['cd /media/build/repo && ./upm makefile --os linux -v | ./upm make --root /media/build/dev --install-dir /pkg -j3 -f -']
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
        
