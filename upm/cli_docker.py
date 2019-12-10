def build_docker(cwd):
   data = y.subprocess.check_output(['docker build .'], cwd=cwd, shell=True, env=y.os.environ).decode('utf-8')
   lines = data.split('\n')
   line = lines[len(lines) - 2]

   print(data.strip(), file=y.stdout)

   return line.split(' ')[2]
   

@y.main_entry_point
async def cli_docker_build(args):
   assert args, 'empty arguments'
   
   root = y.globals.script_dir
   path = root + '/images/'

   for t in args:
      new_ver = build_docker(path + t)

      with y.open_simple_db('~/.upmdb') as db:
         db[t] = db.get(t, []) + [new_ver]

   
@y.main_entry_point
async def cli_docker_run(arg):
   assert arg, 'empty arguments'

   cont = arg[0]
   root = y.globals.script_dir
   path = root + '/images/' + arg[0]

   with y.open_simple_db('~/.upmdb') as data:
      if cont not in data:
         raise Exception('no containers for ' + cont)

      ver = data[cont][-1]
      
   y.os.execv('/bin/bash', ['/bin/bash', path + '/run.sh'] + arg[1:] + [ver])
