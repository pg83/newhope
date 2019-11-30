import os
import subprocess as sp


def get_el(qu):
    while True:
        try:
            return qu.get(True, 0.1)
        except y.queue.Empty:
            pass


class Tasker(object):
    def __init__(self, lst, shell_vars, targets):
        self.lst = lst
        self.shell_vars = shell_vars
        self.targets = targets
        self.t_begin = y.time.time()
        self.build_results = y.build_results_channel()
        
        for i, l in enumerate(self.lst):
            l['n'] = i
    
        self.lst = get_only_our_targets(self.lst, self.targets)
        self.left = len(lst)

        for i, l in enumerate(self.lst):
            l['n'] = i
            
        self.rq, self.wq = y.make_engine(self.lst, lambda x: x['deps1'][0], dep_list=lambda x: sorted(frozenset(x['deps2'])))
        self.process_ready_tasks()

    @property
    def verbose(self):
        return y.verbose
    
    def find_complete(self):
        for x in self.rq():
            yield x
    
    @y.cached_method
    def resolve_path(self, d):
        return subst_vars(d, self.shell_vars)

    def process_result(self, arg):
        if 'll' in arg:
            self.wq(arg['ll']['i'])
            self.process_ready_tasks()

    def process_ready_tasks(self):
        for ll in self.find_complete():
            self.build_results({'new_task': Task(self, ll)})


class Task(object):
    def __init__(self, parent, ll):
        self.ll = ll
        self.p = parent
        self.srch_lst = list(self.iter_deps())
        self.shell = self.find_shell()
        self.env = self.prepare_env()

    @property
    def l(self):
        return self.ll['x']
        
    @property
    def verbose(self):
        return y.verbose
        
    @property
    def shell_vars(self):
        return self.p.shell_vars
        
    def find_tool(self, tool):
        if tool[0] == '/':
            return tool

        return y.find_tool_uncached(tool, self.srch_lst)

    def iter_deps(self):
        for d in self.l['deps2']:
            yield os.path.join(os.path.dirname(self.p.resolve_path(d)), 'bin')

    def find_shell(self):
        if '$YSHELL' in self.shell_vars:
            shell = self.find_tool(self.shell_vars['$YSHELL'])

            if shell:
                return shell
            
            raise Exception('can not find ' + self.shell_vars['$YSHELL'])
            
        return self.find_tool('dash') or self.find_tool('yash') or self.find_tool('sh') or self.find_tool('bash')

    def build_input(self):
        input = '\n'.join(self.l['cmd'])
        
        def iter_parts():
            if '/-x' in self.verbose:
                yield 'set -x'
            else:
                yield 'set +x'
                    
            if '/-v' in self.verbose:
                yield 'set -v'
            else:
                yield 'set +v'

            yield 'set -e'

            for k in sorted(self.env.keys(), key=lambda x: -len(x)):
                yield 'export ' + k + '=' + self.env[k]

            yield 'export BIGI="' + y.base64.b64encode(input.encode('utf-8')).decode('utf-8') + '"'
            yield 'export PATH={runtime}:$PATH'.format(runtime=y.build_scripts_dir())
            yield 'mainfun() {'
            yield input
            yield '}'
            yield 'mainfun ' + ' '.join(y.itertools.chain(self.l['deps1'], self.l['deps2']))

        return '\n'.join(iter_parts()) + '\n'

    def run_cmd(self):
        args = {
            'stdout': sp.PIPE, 
            'stderr': sp.STDOUT,
            'stdin': sp.PIPE,
            'shell': False, 
            'env': self.env, 
            'close_fds': True, 
            'cwd': '/', 
            'bufsize': 1,
        }

        input = self.build_input()
        p = sp.Popen([self.shell, '-s'], **args)
        out = []
        
        try:
            res, _ = p.communicate(input=input.encode('utf-8'))

            if not res.strip():
                res = y.build_run_sh(self.l)

            out.append(res)
            retcode = p.wait()

            if not retcode:
                self.check_results()
        except sp.CalledProcessError as e:
            out.append(e.output)
            retcode = e.returncode
        except Exception:
            out.append(y.format_tbx())
            retcode = -1

        data = '\n'.join(super_decode(o.strip()) for o in out)

        return data, retcode

    def check_results(self):
        for x in self.l['deps1']:
            x = self.p.resolve_path(x)

            try:
                assert os.path.isfile(x)
            except Exception:
                raise Exception(x + ' not exists')
            
    def prepare_env(self):
        return dict(y.itertools.chain({'OUTER_SHELL': self.shell}.items(), fix_shell_vars(self.shell_vars)))
    
    def process_0(self):
        c = self.l.get('cmd')
        tg = self.l['deps1'][0]
        output = self.l['deps1'][0]

        if not c:
            return {'message': 'target {task} complete'.format(task='{w}' + tg + '{}'), 'target': tg}

        if os.path.exists(self.p.resolve_path(output)):
            return {'message': 'target {task} complete'.format(task='{g}' + tg + '{}'), 'target': tg}

        data, retcode = self.run_cmd()
        msg = {}
            
        if data:
            msg.update({
                'text': data,
                'target': tg,
                'command': input,
            })

        if retcode and retcode != -9:
            def shut_down():
                y.time.sleep(10)
                y.stderr.write('{r}bad ' + tg + '{}\n')
                y.os.abort()

            y.threading.Thread(target=shut_down).start()
            
            msg.update({
                'message': 'target {g}' + tg + '{} failed, with retcode ' + str(retcode),
                'status': 'failure',
                'target': tg,
                'retcode': retcode,
            })

        return msg

    def process(self):
        res = self.process_0()
        res.update({'ll': self.ll})
        self.p.build_results(res)


class ThreadPool(object):
    def __init__(self, thrs):                
        self.q = y.queue.SimpleQueue()
        self.threads = [y.threading.Thread(target=self.func) for i in range(0, thrs)]
        self.start()

    def schedule_task(self, task):
        self.q.put(task.process)
            
    def func(self):
        while True:
            try:
                self.q.get()()
            except y.StopNow:
                return
            except Exception as e:
                y.print_tbx()
                y.os.abort()

    def wait_all_threads(self):
        for t in self.threads:
            self.q.put(y.stop_iter)

        for t in self.threads:
            try:
                t.join()
            except Exception:
                pass
            
    def start(self):
        for t in self.threads:
            t.start()

    def join(self):
        kill_all_running()
        self.wait_all_threads()

    def finish(self):
        self.join()

    def process_results(self, arg):
        if 'new_task' in arg:
            self.schedule_task(arg['new_task'])
        
        if arg.get('status', '') == 'build complete':
            self.finish()


async def run_parallel_build(ctl, lst, shell_vars, targets, thrs, bypass_streams):
    tasker = Tasker(lst, shell_vars, targets)
    tpool = ThreadPool(thrs)
    
    def on_timer():
        build_results({'key': 'Left', 'value': str(left)})
        build_results({'key': 'All', 'value': str(len(lst))})
        build_results({'key': 'Complete', 'value': str(len(lst) - left)})
        build_results({'key': 'Wall Clock', 'value': str(y.time.time())})
        build_results({'key': 'Duration', 'value': str(y.time.time() - t_begin)})

    @y.results_callback()
    def tasker_on_result(arg):
        tasker.process_result(arg)

    @y.results_callback()
    def thread_pool_on_result(arg):
        tpool.process_results(arg)
