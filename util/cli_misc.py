@y.main_entry_point
async def cli_cleanup(arg):
   y.os.system("find . | grep '~' | xargs rm")
   y.os.system("find . | grep '#' | xargs rm")


@y.main_entry_point
async def cli_help(args):
   def iter_funcs():
      for f in y.main_entry_points():
         yield f.__name__[4:]

   arg = y.sys.argv[0]
   funcs = sorted(set(iter_funcs()))
   text = 'usage: ' + arg + ' (-v, -vm debug_options)* [' + ', '.join(funcs) + ']'
   
   y.xprint_bg(text)


@y.main_entry_point
async def cli_pip(args):
    import signal

    def ff(a, b):
        return ff
    
    signal.signal = ff
    
    y.sys.argv = ['pip3'] + args
    y.sys.argv[0] = y.re.sub(r'(-script\.pyw?|\.exe)?$', '', y.sys.argv[0])
    
    from pip._internal.main import main

    y.sys.exit(main())
