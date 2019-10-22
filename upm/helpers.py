import os
import sys
import platform
import subprocess

from upm_colors import colorize
from upm_ft import deep_copy, singleton, cached


def to_lines(text):
    def iter_l():
        for l in text.split('\n'):
            l = l.strip()

            if l:
                yield l

    return list(iter_l())


def subst_info(info):
    info = deep_copy(info)

    if 'host' not in info:
        info['host'] = current_host_platform()

    if 'target' not in info:
        info['target'] = deep_copy(info['host'])

    return info


@singleton
def getuser():
    return os.getusername()


def upm_mngr():
    res = {
        'lst': [],
    }

    def on_line(ll):
        if ll.startswith('$(UPM)'):
            res['lst'].append(ll)
        else:
            lst = res['lst']

            if lst:
                if len(lst) > 1:
                    for l in lst:
                        yield l.replace(' #', ' & ')

                    yield '; '.join('wait' for l in lst)
                else:
                    for l in lst:
                        yield l

            res['lst'] = []

            if ll:
                yield ll

    return on_line


@singleton
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
        text = colorize(text, color)

    where.write(text + '\n')


@singleton
def script_path():
   return getattr(sys.modules['__main__'], '__file__')


@cached()
def find_tool(name):
    return subprocess.check_output(['echo `which ' + name + '`'], shell=True).strip()


@singleton
def _tool_binary():
   if sys.argv[0].endswith('upm'):
      return os.path.abspath(sys.argv[0])

   res = os.path.abspath(__file__)

   if 'main.py' in res:
      res = os.path.dirname(os.path.dirname(res)) + '/cli'

   return res


def path_by_script(path):
   return os.path.dirname(script_path()) + '/' + path
