@y.main_entry_point
def cli_cleanup(arg, verbose):
   y.os.system("find . | grep '~' | xargs rm")


@y.main_entry_point
def cli_help(args, verbose):
   def iter_funcs():
      for f in y.main_entry_points():
         yield f.__name__[4:]

   funcs = sorted(set(iter_funcs()))

   y.xxprint('{g}usage: ' + y.sys.argv[0] + ' (-v, --verbose, --profile --bootstrap-mode)* [' + ', '.join(funcs) + '] ..{}')
