def build_docker():
   data = y.subprocess.check_output(['docker build .'], shell=True, env=y.os.environ)
   lines = data.split('\n')
   line = lines[len(lines) - 2]

   y.xprint(data.strip(), where=y.stdout)

   return line.split(' ')[2]


@y.main_entry_point
def cli_build(arg):
   parser = y.argparse.ArgumentParser()

   parser.add_argument('-t', '--target', default=[], action='append', help='add target')
   parser.add_argument('-i', '--image', default='busybox', action='store', help='choose docker image')
   parser.add_argument('-r', '--root', default=None, action='store', help='root for all our data')

   args = parser.parse_args(arg)

   root = args.root

   if not root:
      root = y.upm_root()

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


@y.main_entry_point
def cli_tag(args):
   code = """
       docker tag $1 antonsamokhvalov/newhope:$2
       docker tag antonsamokhvalov/newhope:$2 antonsamokhvalov/newhope:latest
       docker push antonsamokhvalov/newhope:$2
       docker push antonsamokhvalov/newhope:latest
   """.replace('$1', args[0]).replace('$2', args[1])

   y.os.execl('/bin/sh', '/bin/sh', '-c', code)
