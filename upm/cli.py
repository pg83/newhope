import os
import sys
import argparse
import subprocess

from .main import main as main_makefile
from .build import prepare_pkg, get_pkg_link
from .run_make import run_makefile


def build_docker():
   data = subprocess.check_output(['docker build .'], shell=True, env=os.environ)
   lines = data.split('\n')
   line = lines[len(lines) - 2]

   print data.strip()

   return line.split(' ')[2]


def fix_makefile(data):
   path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/cli'
   prefix = '/runtime/cli'

   def iter_lines():
      for l in data.split('\n'):
         p = l.find(prefix)

         if p > 0:
            l = '\t' + path + l[p + len(prefix):]

         yield l

   return '\n'.join(iter_lines()) + '\n'


def cli_make(arg):
   parser = argparse.ArgumentParser()

   parser.add_argument('-j', '--threads', default=1, action='store', help='set num threads')
   parser.add_argument('-f', '--path', default='Makefile', action='store', help='path to Makefile')
   parser.add_argument('--fix-path', default=False, action='store_true')
   parser.add_argument('targets', nargs=argparse.REMAINDER)

   args = parser.parse_args(arg)

   with open(args.path, 'r') as f:
      data = f.read()

   if args.fix_path:
      data = fix_makefile(data)

   run_makefile(data, *args.targets)


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

      data = main_makefile(prefix, args.plugins, False)
      data = fix_makefile(data, prefix)

      run_makefile(data, *args.target)

      return

   def iter_args():
      yield 'docker'
      yield 'run'
      yield '-ti'
      yield '--mount'
      yield 'type=bind,src=' + os.environ['HOME'] + '/repo/packages,dst=/distro/repo'
      yield '--mount'
      yield 'type=bind,src=' + os.getcwd() + '/plugins' + ',dst=/distro/plugins,readonly'

      for n, v in enumerate(args.target):
         yield '--env'
         yield 'TARGET' + str(n + 1) + '=' + v

      yield image

   subprocess.Popen(list(iter_args()), shell=False).wait()


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

   print >>sys.stderr, 'usage: cli [' + ', '.join(iter_funcs()) + '] ....'


def cli_makefile(arg):
   parser = argparse.ArgumentParser()

   parser.add_argument('-o', '--output', default='', action='store', help='file to output, stdout by default')
   parser.add_argument('-P', '--plugins', default='plugins', action='store', help='where to find build rules')
   parser.add_argument('-p', '--prefix', default='', action='store', help='main root for build files')
   parser.add_argument('-k', '--continue-on-fail', default=False, action='store_const', const=True, help='continue on fail')
   parser.add_argument('-b', '--build-only', default=False, action='store_const', const=True, help='just build Makefile')

   args = parser.parse_args(arg)

   prefix = args.prefix

   if prefix.endswith('//'):
      prefix = prefix[:-1]

   data = main_makefile(prefix, args.plugins, args.continue_on_fail)

   if args.build_only:
      print data

      return


def cli_subcommand(args):
   cmds = {}

   for cmd in [prepare_pkg, get_pkg_link]:
      cmds[cmd.__name__] = cmd

   args = args[args.index('--') + 1:]

   cmds[args[0]](*args[1:])


def main():
   mode = sys.argv[1]

   globals().get('cli_' + mode, cli_help)(sys.argv[2:])
