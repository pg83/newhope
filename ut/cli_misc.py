@y.verbose_entry_point
async def cli_misc_cleanup(arg):
   y.os.system("find . | grep '~' | xargs rm")
   y.os.system("find . | grep '#' | xargs rm")
   y.os.system('find . | grep "\\.tmp" | xargs rm')


@y.main_entry_point
async def cli_misc_help(args):
   def iter_funcs():
      allow = 'm'

      if '-v' in y.sys.argv or '-vm' in y.sys.argv:
         allow += 'v'

      mep = y.main_entry_points()
      
      for name in mep:
         t, f = mep[name]
         
         if t in allow:
            yield name.replace('_', ' ')

   arg = y.sys.argv[0]
   funcs = sorted(set(iter_funcs()))
   text = 'usage: ' + arg + ' (-v, -vm debug options)* [command] (command options)*{bb}' + '\n    '.join([''] + funcs) + '{}'
   
   y.xprint_bg(text)


@y.main_entry_point
async def cli_misc_pip(args):
    import signal

    def ff(a, b):
        return ff
    
    signal.signal = ff
    
    y.sys.argv = ['pip3'] + args
    y.sys.argv[0] = y.re.sub(r'(-script\.pyw?|\.exe)?$', '', y.sys.argv[0])

    try:
       from pip._internal.main import main
    except ImportError:
       from pip._internal import main
       
    y.sys.exit(main())


@y.main_entry_point
async def cli_dev_repl(args):
   frame = y.inspect.currentframe()
   frame = frame.f_back

   try:
      from ptpython.repl import embed
   
      embed(frame.f_globals, locals())
   except ImportError:
      y.code.interact(local=frame.f_globals)
   except Exception as e:
      y.debug('in prompt', e)
