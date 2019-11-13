@y.defer_constructor
def init_1():
    if '/psy' in y.verbose:
        y.atexit.register(y.print_stats)
        

@y.defer_constructor
def init_2():
    if '/psd' in y.verbose:
        y.atexit.register(y.print_pub_sub_data)


def select_handler(mode):
   d = dict((f.__name__, f) for f in y.main_entry_points())
   func = 'cli_' + mode

   if func in d:
       f = d[func]

       def wrap(a, b):
           try:
               return f(a, b)
           except TypeError:
               return f(a)

       return wrap

   raise Exception('{mode} unsupported'.format(mode))


def parse_args(args):
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

   if len(args) < 2:
      args = args + ['help']

   return args, verbose, profile


def run_main(args):
   args, verbose, profile = parse_args(args)

   l = locals()

   @y.lookup
   def loopup(name):
      return l[name]

   for f in y.subscribe_queue('deferc', 'main')[0]():
       f['func']()

   func1 = select_handler(args[1])
   func2 = lambda: func1(args[2:], verbose)
   func3 = y.profile(func2, really=profile)

   y.prompt('/p1')
   
   func3()
