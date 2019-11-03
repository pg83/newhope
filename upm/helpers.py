import os
import sys
import platform
import subprocess
import itertools


def find_tool_uncached(tool, path):
    for p in itertools.chain(path, os.environ['PATH'].split(':')):
        pp = os.path.join(p, tool)
        
        if os.path.isfile(pp):
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
    return os.getusername()


@y.singleton
def user_home():
   return os.path.expanduser('~')


@y.singleton
def current_host_platform():
    return {
        'arch': platform.machine(),
        'os': platform.system().lower(),
    }


def fixx(x):
    for f in (str, lambda x: x.decode(utf-8)):
        try:
            x = f(x)
        except Exception:
            pass

    return x


@y.singleton
def script_path():
   if sys.argv[0].endswith('upm'):
      return os.path.abspath(sys.argv[0])

   return sys.modules['__main__'].__file__


@y.singleton
def script_dir():
    return os.path.dirname(script_path())


@y.cached()
def find_tool(name):
    return subprocess.check_output(['which ' + name], shell=True).strip()


def path_by_script(path):
   return script_dir() + '/' + path


@y.singleton
def docker_binary():
   return find_tool('docker')
