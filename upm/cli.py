import os
import sys
import argparse
import subprocess

from .main import main as main_makefile


def cli_build(arg):
   parser = argparse.ArgumentParser()

   parser.add_argument('-t', '--target', default=[], action='append', help='add target')
   parser.add_argument('-i', '--image', default='antonsamokhvalov/newhope:latest', action='store', help='choose docker image')

   args = parser.parse_args(arg)

   def iter_args():
      yield 'docker'
      yield 'run'
      yield '-ti'
      yield '--mount'
      yield 'type=bind,src=/Users/pg/repo/packages,dst=/distro/repo'
      yield '--mount'
      yield 'type=bind,src=/Users/pg/NewHope/newhope/plugins,dst=/distro/plugins'

      for n, v in enumerate(args.target):
         yield '--env'
         yield 'TARGET' + str(n + 1) + '=' + v

      yield args.image

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
   parser.add_argument('-P', '--plugins', default='', action='store', help='where to find build rules')
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


def main():
   mode = sys.argv[1]

   globals().get('cli_' + mode, cli_help)(sys.argv[2:])
