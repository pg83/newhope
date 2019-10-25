import os
import sys
import platform
import subprocess

from upm_iface import y


def to_lines(text):
    def iter_l():
        for l in text.split('\n'):
            l = l.strip()

            if l:
                yield l

    return list(iter_l())


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


def xprint(*args, **kwargs):
    def fixx(x):
        try:
            x = str(x)
        except:
            pass

        try:
            x = x.decode('utf-8')
        except:
            pass

        return x

    color = kwargs.get('color')
    where = kwargs.get('where', sys.stderr)
    text = ' '.join([fixx(x) for x in args])

    if color:
        text = y.colorize(text, color)

    where.write(text + '\n')


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
