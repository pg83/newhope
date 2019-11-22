@y.main_entry_point
def cli_run(args):
   try:
      ids = args.index('--root')
      root = args[ids + 1]
      args = args[:ids] + args[2:]
   except Exception as e:
      root = y.upm_root()

   def iter_args():
      yield 'docker'
      yield 'run'
      yield '--mount'
      yield 'type=bind,src=' + root + ',dst=/d'

      for x in args:
         yield x

   y.os.execl(y.docker_binary(), *list(iter_args()))
