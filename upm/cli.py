def build_docker():
   data = y.subprocess.check_output(['docker build .'], shell=True, env=y.os.environ)
   lines = data.split('\n')
   line = lines[len(lines) - 2]

   y.xprint(data.strip(), where=y.sys.stdout)

   return line.split(' ')[2]


def prepare_root(r):
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
      except Exception:
         y.print_tbx(tb_line='can not run ' + a)


@y.main_entry_point
def cli_cleanup(arg, verbose):
   y.os.system("cd {sd} && (find . | grep '~' | xargs rm)".format(sd=y.script_dir()))


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
   data = {'file_data': y.file_data, 'data': y.stagea.__ytext__}
   data = y.marshal.dumps(data)
   data = y.zlib.compress(data)
   data = y.base64.b64encode(data)

   code = 'import marshal; import zlib; import base64; fd = marshal.loads(zlib.decompress(base64.b64decode("{data}"))); file_data = fd["file_data"]; data = fd["data"]'
   code = code.replace('{data}', data)

   for x in y.file_data:
      if x['path'] == 'cli':
         break

   print x['data'].replace('#REPLACEME', code)
   

def run_main(args):
   args, verbose = y.check_arg(args, ('-v', '--verbose'))
   args, profile = y.check_arg(args, ('--profile',))
   args, verbose_mode = y.check_arg_2(args, '-vm', True)

   if verbose_mode is None:
      args, verbose_mode = y.check_arg_2(args, '--verbose-mode', True)

   if verbose_mode:
      verbose = verbose_mode
   else:
      if verbose:
         verbose = '1'
      else:
         verbose = ''

   l = locals()

   @y.lookup
   def loopup(name):
      return l[name]

   if len(args) < 2:
      args = args + ['help']

   mode = args[1]

   def func():
      def select():
         d = dict((f.__name__, f) for f in y.main_entry_points())
         func = 'cli_' + mode

         if func in d:
            return d[func]
         
         raise Exception('{mode} unsupported'.format(mode))
         
      ff = select()
      ff(args[2:], verbose)

   func = y.profile(func, really=profile)
   func = y.logged_wrapper(rethrow=-1, rfunc=func, important=True)

   y.run_all_defer_constructors()
   y.prompt('/p1')
   
   func()
