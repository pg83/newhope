def find_tool_uncached(tool, path):
    for p in y.itertools.chain(path, y.os.environ['PATH'].split(':')):
        pp = y.os.path.join(p, tool)
        
        if y.os.path.isfile(pp):
            return pp


def subst_info(info):
    info = y.deep_copy(info)

    if 'host' not in info:
        info['host'] = current_host_platform()

    if 'target' not in info:
        info['target'] = y.deep_copy(info['host'])

    return info


@y.singleton
def getuser():
    return y.os.getusername()


@y.singleton
def user_home():
   return y.os.path.expanduser('~')


def upm_root():
   return user_home() + '/upm_root'


@y.singleton
def current_host_platform():
    return {
        'arch': y.platform.machine(),
        'os': y.platform.system().lower(),
    }


def fixx(x):
    for f in (str, lambda x: x.decode(utf-8)):
        try:
            x = f(x)
        except Exception:
            pass

    return x


@y.singleton
def script_dir():
    return y.os.path.dirname(y.script_path)


@y.cached()
def find_tool(name):
    return find_tool_uncached(name, [])


def path_by_script(path):
   return script_dir() + '/' + path


@y.singleton
def docker_binary():
   return find_tool('docker')
