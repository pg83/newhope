def build_docker(cwd):
    data = y.subprocess.check_output(['docker build .'], cwd=cwd, shell=True, env=y.os.environ).decode('utf-8')
    lines = data.split('\n')
    line = lines[len(lines) - 2]

    print(data.strip(), file=y.stdout)

    return line.split(' ')[2]


def path_to_images():
    return y.globals.script_dir + '/images'


@y.main_entry_point
async def cli_docker_build(args):
    assert args, 'empty arguments'

    path = path_to_images()

    for t in args:
        new_ver = build_docker(path + t)

        with y.open_pdb() as db:
            db.images[t] = db.images.get(t, []) + [new_ver]


def data_for_container(cont):
   path = path_to_images() + '/' + cont
   
   with y.open_pdb() as db:
       if cont not in db.images:
           raise Exception('no containers for ' + cont)

       return {'data': db.images[cont], 'path': path}


@y.main_entry_point
async def cli_docker_run(arg):
   assert arg, 'empty arguments'

   cont = arg[0]
   data = data_for_container(cont)
   path = data['path']
   latest = data['data'][-1]

   y.os.execv('/bin/bash', ['/bin/bash', path + '/run.sh'] + arg[1:] + [latest])


def get_running():
    out = y.subprocess.check_output(['docker container ls'], shell=True).decode('utf-8')
    res = dict((y[0], y[1]) for y in (x.split() for x in out.split('\n')[1:] if x))

    return res
   
   
@y.main_entry_point
async def cli_docker_list(arg):
    info = get_running()

    def is_running(cont):
        try:
            return data_for_container(cont)['data'][-1] in info.keys()
        except Exception:
            return False
        
    for i in y.os.listdir(path_to_images()):
        print(is_running(i), '{bb}' + i + '{}')


@y.main_entry_point
async def cli_docker_shell(arg):
    assert arg, 'empty arguments'
