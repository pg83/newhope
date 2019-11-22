@y.main_entry_point
def cli_cleanup(arg):
   y.os.system("find . | grep '~' | xargs rm")


@y.main_entry_point
def cli_help(args):
   def iter_funcs():
      for f in y.main_entry_points():
         yield f.__name__[4:]

   arg = y.sys.argv[0]
   funcs = sorted(set(iter_funcs()))

   y.xprint_g('usage: ' + arg + ' (-v, --verbose, --profile --bootstrap-mode)* [' + ', '.join(funcs) + ']')
