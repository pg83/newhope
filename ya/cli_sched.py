def proc_func(code):
    def do():
        y.info('will run', code)
        p = y.subprocess.Popen(code, shell=True)
        retcode = p.wait()
        y.info('done, with code', retcode)
        y.time.sleep(1)

    return do


def wait_pid():
    for i in range(0, 10):
        y.debug('got something', y.os.waitpid(0, y.os.WNOHANG))

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
    ['/media/build/upm cmd rmtmp /media/build/r && sleep 600'],
    ['/media/build/upm cmd rmtmp /media/storage && sleep 700'],
    ['/usr/bin/timeout 30m /media/build/upm pkg serve repo --fr /media/storage --port 10000'],
    ['cd /media/build && ./upm makefile --os linux -v > ./Makefile.tmp && mv ./Makefile.tmp ./Makefile && sleep 30'],
    ['cd /media/build && ./upm make --keep-going --root /media/build --install-dir /pkg -j10 -f ./Makefile -v'],
]


BUILD = [
    wait_pid,
    watch_dog,
] + [proc_func(x) for x in BUILD_PROC]


DOCKER = BUILD[2:]


TEST_PROC = [
    proc_func(['sleep 1']),
    proc_func(['sleep 2']),
    proc_func(['sleep 3']),
]


def run_subrule(code, num):
    y.find(code)[num]()


def run_runit(args):
    tool = y.find_tool('runsvdir')[0]
    path = y.os.path.abspath(y.os.getcwd())

    def iter_it():
        for t in args.targets:
            for i, c in enumerate(y.find(t)):
                folder = t.lower() + '_' + str(i)
                cmd = y.sys.argv
                cmd = cmd[:cmd.index('scheduler') + 1] + ['--num', str(i), t]

                yield folder, cmd

    for folder, cmd in iter_it():
        data = '#!/bin/sh\n\nexec ' + ' '.join(cmd) + '\n'
        p = y.os.path.join(path, folder)

        try:
            y.os.makedirs(p)
        except OSError:
            pass

        f = y.os.path.join(p, 'run')

        y.write_file(f, data, mode='w')
        y.os.chmod(f, 0o744)

    y.os.execl(tool, tool, path)


@y.verbose_entry_point
def cli_cmd_scheduler(arg):
    p = y.argparse.ArgumentParser()

    p.add_argument('-r', '--runit', default=False, action='store_const', const=True, help='use runit infra')
    p.add_argument('-n', '--num', default=None, action='store', help='subrule number')
    p.add_argument('targets', nargs=y.argparse.REMAINDER)

    args = p.parse_args(arg)

    if args.num is not None:
        run_subrule(args.targets[0], int(args.num))
    elif args.runit:
        run_runit(args)
    else:
        run_threads(args.targets)


def wrap_inf(func):
    def wrapper():
        while True:
            try:
                func()
            except Exception as e:
                y.warning('in scheduler ' + func.__name__ + ', ' + str(e))
                y.time.sleep(1)

    return wrapper


def run_threads(args):
    y.os.nice(20)
    code = (len(args) > 0 and args[0]) or 'ENTRY'
    y.info('code', code)

    thrs = [y.threading.Thread(target=wrap_inf(c)) for c in y.find(code)]

    for t in thrs:
        t.start()

    for t in thrs:
        t.join()
