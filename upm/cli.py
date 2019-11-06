def build_docker():
   data = y.subprocess.check_output(['docker build .'], shell=True, env=y.os.environ)
   lines = data.split('\n')
   line = lines[len(lines) - 2]

   y.xprint(data.strip(), where=y.sys.stdout)

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
         yield y.os.path.join(r, f)

   for f in iter_trash():
      try:
         y.shutil.rmtree(f)
      except Exception as e:
         if 'No such file or directory' in str(e):
            pass
         else:
            y.xprint_red(f, e)

   for f in ('bin', 'tmp'):
      try:
         y.os.makedirs(y.os.path.join(r, f))
      except OSError:
         pass

   p = y.os.path.join(r, 'bin', 'upm')

   with open(p, 'w') as f:
      f.write(data)
      y.os.system('chmod +x ' + p)


@y.main_entry_point
def cli_eval(args, verbose):
   repl = {
      'layers': 'y.gen_all_texts(only_print_layers=True)'
   }

   if not args:
      for k, v in repl.items():
         y.xxprint(k, '=', v, init='b')

      return

   for a in args:
      try:
         print eval(repl.get(a, a))
      except Exception as e:
         y.xprint_red('can not run ' + a, y.traceback.format_exc(e))


@y.main_entry_point
def cli_cleanup(arg, verbose):
   y.os.system("cd {sd} && (find . | grep '~' | xargs rm)".format(sd=y.script_dir()))


@y.main_entry_point
def cli_run(args, verbose):
   try:
      ids = args.index('--root')
      root = args[ids + 1]
      args = args[:ids] + args[2:]
   except Exception as e:
      root = y.upm_root()

   prepare_root(root)

   def iter_args():
      yield 'docker'
      yield 'run'
      yield '--mount'
      yield 'type=bind,src=' + root + ',dst=/d'

      for x in args:
         yield x

   y.os.execl(docker_binary(), *list(iter_args()))


@y.main_entry_point
def cli_tag(args, verbose):
   code = """
       docker tag $1 antonsamokhvalov/newhope:$2
       docker tag antonsamokhvalov/newhope:$2 antonsamokhvalov/newhope:latest
       docker push antonsamokhvalov/newhope:$2
       docker push antonsamokhvalov/newhope:latest
   """.replace('$1', args[0]).replace('$2', args[1])

   y.os.execl('/bin/sh', '/bin/sh', '-c', code)


@y.main_entry_point
def cli_help(args, verbose):
   def iter_funcs():
      for f in y.main_entry_points():
         yield f.__name__[4:]
         
   y.xprint_green('usage: ' + y.sys.argv[0] + ' (-v, --verbose, --profile --bootstrap-mode)* ' + '[' + ', '.join(sorted(set(iter_funcs()))) + '] ....')


@y.main_entry_point
def cli_release(args, verbose):
   print y.rm_prepare_release_data() + '\n\nbootstrap(0)\n\n'


def run_main(args):
   args, verbose = y.check_arg(args, ('-v', '--verbose'))
   args, profile = y.check_arg(args, ('--profile',))
   args, verbose_mode = y.rm_check_arg_2(args, '-vm', True)

   if verbose_mode is None:
      args, verbose_mode = y.rm_check_arg_2(args, '--verbose-mode', True)

   if verbose_mode: 
      verbose = verbose_mode
   else:
      if verbose:
         verbose = '1'
      else:
         verbose = ''

   if len(args) < 2:
      args = args + ['help']

   mode = args[1]

   def func():
      def select():
         d = dict((f.__name__, f) for f in y.main_entry_points())

         return d['cli_' + mode]

      ff = select()
      ff(args[2:], verbose)

   func = y.profile(func, really=profile)
   func = y.logged_wrapper(rethrow=-1, tb=verbose, rfunc=func, important=True)
   
   l = locals()

   @y.lookup
   def find(name):
      return l[name]

   y.run_all_defer_constructors()

   return func()
