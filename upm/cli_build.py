@y.main_entry_point
def cli_build(arg, verbose):
   parser = y.argparse.ArgumentParser()

   parser.add_argument('-t', '--target', default=[], action='append', help='add target')
   parser.add_argument('-i', '--image', default='busybox', action='store', help='choose docker image')
   parser.add_argument('-r', '--root', default=None, action='store', help='root for all our data')

   args = parser.parse_args(arg)

   root = args.root

   if not root:
      root = y.upm_root()

   y.prepare_root(root)

   image = args.image

   if image == "now":
      image = y.build_docker()

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

   y.subprocess.Popen(list(iter_args()), shell=False).wait()
