import os
import sys
import argparse
import subprocess


def build(arg):
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


def tag(args):
   code = """
       docker tag $1 antonsamokhvalov/newhope:$2
       docker tag antonsamokhvalov/newhope:$2 antonsamokhvalov/newhope:latest
       docker push antonsamokhvalov/newhope:$2
       docker push antonsamokhvalov/newhope:latest
   """.replace('$1', args[0]).replace('$2', args[1])

   os.execl('/bin/bash', '/bin/bash', '-c', code)


def help1(args):
   print >>sys.stderr, 'usage: cli [build, ] ....'


def main():
   mode = sys.argv[1]

   globals().get(mode, help1)(sys.argv[2:])
