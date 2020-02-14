@y.verbose_entry_point
def cli_misc_cleanup(arg):
   y.os.system("find . | grep '~' | xargs rm")
   y.os.system("find . | grep '#' | xargs rm")
   y.os.system('find . | grep "\\.tmp" | xargs rm')

   def fix1(data):
      return data.replace('    \n', '\n')

   def fix2(data):
      return data.replace("\t", '    ')
   
   fixers = [
      fix1,
      fix2,
   ]
   
   for a, b, c in y.os.walk('.'):
      for x in c:
         pp = y.os.path.join(a, x)

         if pp.endswith('.py'):
            with open(pp, 'r') as f:
               orig = f.read()

            data = orig
   
            for i in range(0, 2):
               for j in fixers:
                  data = j(data)

            if data != orig:
               with open(pp + '.$tmp', 'w') as f:
                  f.write(data)

               y.os.rename(pp + '.$tmp', pp)
   

@y.main_entry_point
def cli_misc_help(args):
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
def cli_misc_pip(args):
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
def cli_dev_repl(args):
   frame = y.inspect.currentframe()
   frame = frame.f_back

   try:
      from ptpython.repl import embed
   
      embed(frame.f_globals, locals())
   except ImportError:
      y.code.interact(local=frame.f_globals)
   except Exception as e:
      y.debug('in prompt', e)

  
@y.verbose_entry_point
async def cli_misc_timeout(args):
    import os

    tout = int(args[0])
    pid = os.fork()

    if pid:
        y.time.sleep(tout)
        os.kill(pid, y.signal.SIGINT)
        os.waitpid(pid, 0)
        os._exit(0)
    else:
        os.execv(args[1], args[1:])
