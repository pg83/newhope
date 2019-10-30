import os
import imp
import sys
import traceback
import argparse
import subprocess
import shutil
import traceback
import urllib2


def build_docker():
   data = subprocess.check_output(['docker build .'], shell=True, env=os.environ)
   lines = data.split('\n')
   line = lines[len(lines) - 2]

   y.xprint(data.strip(), where=sys.stdout)

   return line.split(' ')[2]


def prepare_root(r):
   try:
      data = y.rm_prepare_release_data() + '\n\nbootstrap(0)\n'
   except Exception as e:
      if 'unimplemented' not in str(e):
         raise

      return

   def iter_trash():
      for f in ('w', 'd', 'bin', 'tmp'):
         yield os.path.join(r, f)

   for f in iter_trash():
      try:
         shutil.rmtree(f)
      except Exception as e:
         if 'No such file or directory' in str(e):
            pass
         else:
            y.xprint_red(f, e)

   for f in ('bin', 'tmp'):
      try:
         os.makedirs(os.path.join(r, f))
      except OSError:
         pass

   p = os.path.join(r, 'bin', 'upm')

   with open(p, 'w') as f:
      f.write(data)
      os.system('chmod +x ' + p)

   #os.execl(p, *([p] + sys.argv[1:]))


def fetch_1(url):
   return urllib2.urlopen(url).read()


def fetch_2(url):
   return subprocess.check_output(['curl -o - ' + url], shell=True)


def fetch_data(url):
   for f in (fetch_1, fetch_2):
      try:
         return f(url)
      except Exception as e:
         print e

   if e:
      raise e


def fetch_http(root, url):
   name = os.path.basename(url)
   fname = os.path.join(root, name)
   data = fetch_data(url)

   try:
      os.makedirs(root)
   except OSError:
      pass

   with open(fname, 'w') as f:
      f.write(data)

   subprocess.check_output(['tar -xf ' + name], cwd=root, shell=True)

   return url


def cli_fetch(arg, verbose):
   parser = argparse.ArgumentParser()

   parser.add_argument('--path', default='data', action='store', help='Where to store all')
   parser.add_argument('targets', nargs=argparse.REMAINDER)

   args = parser.parse_args(arg)
   args.path = os.path.abspath(args.path)

   def iter_urls():
      host = y.current_host_platform()
      target = host
      cc = {'host': host, 'target': target}
      params = {'info': cc, 'compilers': {'deps': [], 'cross': False}}

      for t in args.targets:
         if t.startswith('http'):
            yield fetch_http(args.path, url)
         else:
            node = y.restore_node(eval('y.' + t)(y.deep_copy(params)))['node']()
            url = node.get('src') or node.get('url')
            yield fetch_http(args.path, url)

   for url in iter_urls():
      print 'done', url


def cli_make(arg, verbose):
   parser = argparse.ArgumentParser()

   parser.add_argument('-j', '--threads', default=1, action='store', help='set num threads')
   parser.add_argument('-f', '--path', default='Makefile', action='store', help='path to Makefile')
   parser.add_argument('-k', '--continue-on-fail', default=False, action='store_const', const=True, help='continue on fail')
   parser.add_argument('-r', '--root', default=None, action='store', help='main root for build files')
   parser.add_argument('-i', '--install-dir', default=None, action='store', help='where to install packages')
   parser.add_argument('-d', '--do-not-remove', default=None, action='store', help='не удалять даннные')
   parser.add_argument('--production', default=False, action='store_const', const=True, help='production execution')
   parser.add_argument('targets', nargs=argparse.REMAINDER)

   args = parser.parse_args(arg)
   local = not args.production

   if local and args.install_dir:
      raise Exception('do not do this, kids, at home')

   def calc_root():
      if args.root:
         return args.root

      if local:
         return upm_root()

      if args.production:
         return '/d'

      raise Exception('can not determine root')

   root = calc_root()
   prepare_root(root)

   def iter_replaces():
      if args.install_dir:
         yield ('$(WDP)', args.install_dir)

      yield ('$(WDM)', '$(PREFIX)/m')
      yield ('$(WDR)', '$(PREFIX)/r')
      yield ('$(WDW)', '$(PREFIX)/w')

      if local:
         yield ('$(WDP)', '$(PREFIX)/p')
         yield ('$(UPM)', y.script_path())

         if args.do_not_remove:
            yield ('$(RM_TMP)', '# ')
         else:
            yield ('$(RM_TMP)', 'rm -rf')

      if args.production:
         yield ('$(WDP)', '/private')
         yield ('$(UPM)', 'upm')
         yield ('$(RM_TMP)', '# ')

      yield ('$(PREFIX)', root)
      yield ('$$', '$')

   if args.path == '-':
      data = sys.stdin.read()
   elif args.path:
      with open(args.path, 'r') as f:
         data = f.read()
   else:
      data = sys.stdin.read()

   y.run_makefile(y.subst_kv_base(data, iter_replaces()), [], args.targets)


def upm_root():
   return y.user_home() + '/upm_root'


def cli_build(arg, verbose):
   parser = argparse.ArgumentParser()

   parser.add_argument('-t', '--target', default=[], action='append', help='add target')
   parser.add_argument('-i', '--image', default='busybox', action='store', help='choose docker image')
   parser.add_argument('-r', '--root', default=None, action='store', help='root for all our data')

   args = parser.parse_args(arg)

   root = args.root

   if not root:
      root = upm_root()

   prepare_root(root)

   image = args.image

   if image == "now":
      image = build_docker()

   def iter_args():
      yield 'docker'
      yield 'run'
      yield '-ti'
      yield '--mount'
      yield 'type=bind,src=' + root + ',dst=/d'

      for n, v in enumerate(args.target):
         yield '--env'
         yield 'TARGET' + str(n + 1) + '=' + v

      yield image

   subprocess.Popen(list(iter_args()), shell=False).wait()


def cli_run(args, verbose):
   try:
      ids = args.index('--root')
      root = args[ids + 1]
      args = args[:ids] + args[2:]
   except Exception as e:
      root = upm_root()

   prepare_root(root)

   def iter_args():
      yield 'docker'
      yield 'run'
      yield '--mount'
      yield 'type=bind,src=' + root + ',dst=/d'

      for x in args:
         yield x

   os.execl(docker_binary(), *list(iter_args()))


def cli_tag(args, verbose):
   code = """
       docker tag $1 antonsamokhvalov/newhope:$2
       docker tag antonsamokhvalov/newhope:$2 antonsamokhvalov/newhope:latest
       docker push antonsamokhvalov/newhope:$2
       docker push antonsamokhvalov/newhope:latest
   """.replace('$1', args[0]).replace('$2', args[1])

   os.execl('/bin/sh', '/bin/sh', '-c', code)


def cli_help(args, verbose):
   def iter_funcs():
      for k in sorted(globals().keys()):
         if k.startswith('cli_'):
            yield k[4:]

   y.xprint_green('usage: ' + sys.argv[0] + ' (-v, --verbose, --profile --bootstrap-mode)* ' + '[' + ', '.join(iter_funcs()) + '] ....')


def cli_makefile(arg, verbose):
   parser = argparse.ArgumentParser()

   parser.add_argument('-o', '--output', default='', action='store', help='file to output, stdout by default')
   parser.add_argument('-S', '--shell', default=[], action='append', help='out build.sh script')
   parser.add_argument('-P', '--plugins', default=[], action='append', help='where to find build rules')

   args = parser.parse_args(arg)

   if args.output:
      f = open(args.output, 'w')
      close = f.close
   else:
      f = sys.stdout
      close = lambda: 0

   try:
      if args.shell:
         f.write(y.build_sh_script(args.shell), verbose)
      else:
         f.write(y.main_makefile(verbose))

      f.flush()
   finally:
      close()


def cli_release(args, verbose):
   print y.rm_prepare_release_data() + '\n\nbootstrap(0)\n\n'


def cli_selftest(args, verbose):
   for f in y.iter_all_tests():
      y.xprint_white('-------------------------------------------------------------------')
      f()

   y.xprint_white('-------------------------------------------------------------------')


def run_main(args):
   args, do_verbose = y.check_arg(args, ('-v', '--verbose'))
   args, do_profile = y.check_arg(args, ('--profile',))

   if len(args) < 2:
      args = args + ['help']

   mode = args[1]

   def func():
      ff = globals().get('cli_' + mode, cli_help)
      ff(args[2:], do_verbose)

   func = y.profile(func, really=do_profile)
   func = y.logged_wrapper(rethrow=-1, tb=True, rfunc=func)

   return func()
