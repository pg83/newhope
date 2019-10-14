import os
import sys
import argparse
import subprocess

from .main import main as main_makefile
from .build import prepare_pkg, get_pkg_link
from .run_make import run_makefile
from .user import singleton
from .colors import RED, RESET


try:
   from .release_me import prepare_data
except ImportError:
   def prepare_data():
      with open(os.path.abspath(__file__), 'r') as f:
         return f.read()


@singleton
def docker_binary():
   return subprocess.check_output(['/bin/sh -c "which docker"'], shell=True).strip()


@singleton
def tool_binary():
   res = os.path.abspath(__file__)

   if 'cli.py' in res:
      res = os.path.dirname(os.path.dirname(res)) + '/cli'

   return res


def build_docker():
   try:
      with open('upm/upm', 'w') as f:
         f.write(prepare_data())

      os.system('chmod +x upm/upm')

      data = subprocess.check_output(['docker build .'], shell=True, env=os.environ)
      lines = data.split('\n')
      line = lines[len(lines) - 2]

      print data.strip()

      return line.split(' ')[2]
   finally:
      os.unlink('upm/upm')


def cli_make(arg):
   parser = argparse.ArgumentParser()

   parser.add_argument('-j', '--threads', default=1, action='store', help='set num threads')
   parser.add_argument('-f', '--path', default='Makefile', action='store', help='path to Makefile')
   parser.add_argument('targets', nargs=argparse.REMAINDER)

   args = parser.parse_args(arg)

   with open(args.path, 'r') as f:
      data = f.read()

   run_makefile(data, tool_binary(), *args.targets)


def cli_build(arg):
   parser = argparse.ArgumentParser()

   parser.add_argument('-t', '--target', default=[], action='append', help='add target')
   parser.add_argument('-i', '--image', default='antonsamokhvalov/newhope:latest', action='store', help='choose docker image')
   parser.add_argument('-P', '--plugins', default='plugins', action='store', help='where to find build rules')
   parser.add_argument('-p', '--prefix', default='', action='store', help='main root for build files')

   args = parser.parse_args(arg)
   image = args.image

   if image == "now":
      image = build_docker()
   elif image == 'system':
      prefix = args.prefix

      if not prefix:
         raise Exception('prefix is mandatory in local mode')

      data = main_makefile(prefix, args.plugins, False, rm_tmp='rm -rf', install_dir='$(PREFIX)/i')

      return run_makefile(data, tool_binary(), *args.target)

   def iter_args():
      yield 'docker'
      yield 'run'
      yield '-ti'
      yield '--mount'
      yield 'type=bind,src=' + os.environ['HOME'] + '/repo,dst=/d/r'
      yield '--mount'
      yield 'type=bind,src=' + os.getcwd() + '/plugins' + ',dst=/d/p,readonly'

      for n, v in enumerate(args.target):
         yield '--env'
         yield 'TARGET' + str(n + 1) + '=' + v

      yield image

   subprocess.Popen(list(iter_args()), shell=False).wait()


def cli_run(args):
   def iter_args():
      yield 'docker'
      yield 'run'
      yield '--mount'
      yield 'type=bind,src=' + os.environ['HOME'] + '/repo,dst=/d/r'
      yield '--mount'
      yield 'type=bind,src=' + os.getcwd() + '/plugins' + ',dst=/d/p,readonly'

      for x in args:
         yield x

   os.execl(docker_binary(), *list(iter_args()))


def cli_tag(args):
   code = """
       docker tag $1 antonsamokhvalov/newhope:$2
       docker tag antonsamokhvalov/newhope:$2 antonsamokhvalov/newhope:latest
       docker push antonsamokhvalov/newhope:$2
       docker push antonsamokhvalov/newhope:latest
   """.replace('$1', args[0]).replace('$2', args[1])

   os.execl('/bin/bash', '/bin/bash', '-c', code)


def cli_help(args):
   def iter_funcs():
      for k in sorted(globals().keys()):
         if k.startswith('cli_'):
            yield k[4:]

   print >>sys.stderr, 'usage: ' + sys.argv[0] + ' [' + ', '.join(iter_funcs()) + '] ....'


def cli_makefile(arg):
   parser = argparse.ArgumentParser()

   parser.add_argument('-o', '--output', default='', action='store', help='file to output, stdout by default')
   parser.add_argument('-P', '--plugins', default='$(PREFIX)/p', action='store', help='where to find build rules')
   parser.add_argument('-p', '--prefix', default='', action='store', help='main root for build files')
   parser.add_argument('-k', '--continue-on-fail', default=False, action='store_const', const=True, help='continue on fail')
   parser.add_argument('-l', '--local', default=False, action='store_const', const=True, help='makefile for local execution')
   parser.add_argument('-i', '--install-dir', default='$(PREFIX)/i', action='store', help='where to install packages')

   args = parser.parse_args(arg)

   prefix = args.prefix

   if prefix.endswith('//'):
      prefix = prefix[:-1]

   if args.local:
      rm_tmp = 'rm -rf'
   else:
      rm_tmp = '# '

   if args.output:
      f = open(args.output, 'w')
   else:
      f = sys.stdout

   f.write(main_makefile(prefix, args.plugins, args.continue_on_fail, rm_tmp, args.install_dir))


def cli_subcommand(args):
   cmds = {}

   for cmd in [prepare_pkg, get_pkg_link]:
      cmds[cmd.__name__] = cmd

   args = args[args.index('--') + 1:]

   cmds[args[0]](*args[1:])


def cli_release(args):
   print prepare_data()


def run_main():
   if len(sys.argv) < 2:
      args = sys.argv + ['help']
   else:
      args = sys.argv

   new_args = list(filter(lambda x: x not in ('-v', '--verbose'), args))
   verbose = len(args) != len(new_args)
   args = new_args

   mode = args[1]

   def func():
      globals().get('cli_' + mode, cli_help)(args[2:])

   if verbose:
      func()
   else:
      try:
         func()
      except Exception as e:
         print RED + str(e) + RESET

      return 1

   return 0
