def build_docker(cwd):
   data = y.subprocess.check_output(['docker build .'], cwd=cwd, shell=True, env=y.os.environ).decode('utf-8')
   lines = data.split('\n')
   line = lines[len(lines) - 2]

   print(data.strip(), file=y.stdout)

   return line.split(' ')[2]


@y.main_entry_point
async def cli_build(args):
   root = y.os.path.abspath(y.os.getcwd())
   path = root + '/images/'

   for t in args:
      print build_docker(path + t)
      
   
@y.main_entry_point
async def cli_run(arg):
   root = y.os.path.abspath(y.os.getcwd())
   path = root + '/images/' + arg[0]
   
   y.os.execv('/bin/bash', ['/bin/bash', path + '/run.sh'] + arg[1:])
