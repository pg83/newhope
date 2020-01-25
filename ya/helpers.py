def find_tool_uncached_0(tool, path):
    for p in y.itertools.chain(path, y.os.environ['PATH'].split(':')):
        pp = y.os.path.join(p, tool)

        if y.os.path.isfile(pp):
            yield pp


def find_tool_uncached(tool, path):
    for x in find_tool_uncached_0(tool, path):
        return x


@y.singleton
def getuser():
    return y.os.getusername()


@y.singleton
def user_home():
   return y.os.path.expanduser('~')


def upm_root():
   return user_home() + '/upm_root'


@y.cached()
def find_tool(name):
    return list(find_tool_uncached_0(name, []))


@y.singleton
def docker_binary():
    return find_tool('docker')[0]
