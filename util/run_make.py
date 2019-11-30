async def run_makefile(data, shell_vars, targets, threads, parsed, pre_run=[]):
    async def run_build_2(ctl):
        lst = data
            
        if not parsed:
            lst = await y.parse_makefile(lst)
                    
        await y.cheet(lst)
    
        if pre_run:
            return await run_par_build(ctl, await y.select_targets(lst, pre_run), shell_vars, pre_run, 1)

        y.os.abort()
        print 7
        return await run_par_build(ctl, await y.select_targets(lst, targets), shell_vars, targets, threads)

    return await y.spawn(run_build_2, 'build')


class Fail(Exception):
    pass


class Builder(object):
    def __init__(self, ctl, lst, shell_vars, targets, threads):
        self.thr = threads
        self.ctl = ctl
        self.shell_vars = shell_vars
        self.targets = targets
        self.build_results = y.build_results_channel()
        self.lst = [item_factory(x, self) for x in lst]

        by_dep = {}

        def iter_items():
            for x in lst:
                yield item_factory(x, self)

            yield item_factory({'cmd': [], 'deps1': ['all'], 'deps2': sorted(list(by_dep.keys()))}, self)
                
        for x in iter_items():
            for d in x.deps1:
                by_dep[d] = x

        for k in by_dep.keys():
            self.resolve_path(k)

        self.by_dep = by_dep
        
    @y.cached_method
    def resolve_path(self, d):
        return y.subst_vars(d, self.shell_vars)

    async def run(self):
        done = set()
        channel = [y.collections.deque() for x in range(0, self.thr)]
        hndl = []
        unready = y.collections.deque(self.by_dep.keys())
        
        def iter_deque(d):
            try:
                while d:
                    yield d.popleft()
            except IndexError:
                pass
        
        def iter_all_channels():
            for c in channel:
                for x in iter_deque(c):
                    yield x
                
        def iter_next(my):
            for el in iter_deque(unready):
                if y.os.path.exists(self.resolve_path(el)):
                    my.append(el)

                    continue
                
                yield el

        def is_in(a, b):
            for x in a:
                if x not in b:
                    return False

            return True
                
        for x in enumerate(channel):
            def builder(num, my):
                async def runner(ctl):
                    async def run(el):
                        print el, done
                        
                        n = self.by_dep[el]
                        deps = frozenset(n.deps2)

                        if not is_in(deps, done):
                            unready.append(el)

                            return
                    
                        if await n.run_cmd():
                            raise Fail()
                            
                        for d in n.deps1:
                            my.append(d)
                            
                        my.append(el)

                    while True:
                        v = set()
                        
                        for el in iter_next(my):
                            if el in v:
                                break
                            
                            v.add(el)

                            await run(el)
                            
                        await ctl.sleep(0.1)

                return runner, 'runner_' + str(num)

            hndl.append(self.ctl.spawn(*builder(*x)))

        while True:
            new_done = y.copy.copy(done)

            for dep in iter_all_channels():
                if dep == 'fail':
                    self.on_build_status(True)
                    
                    return dep

                if dep == 'all':
                    self.on_build_status(False)
                
                    return dep
                
                new_done.add(dep)

            done = new_done
            print done, 'here in'
            await self.ctl.sleep(0.1)
            print 'here out'
            
    def on_build_status(self, fail):
        if fail:
            self.build_results({'message': 'all ok', 'status': 'ok'})
        else:
            self.build_results({'message': 'build not finished', 'status': 'failure'})


def item_factory(n, p):
    if n.get('cmd'):
        return Item(n, p)

    return ItemBase(n)
            

class ItemBase(object):
    def __init__(self, n):
        self.n = n

    @property
    def my_name(self):
        return ', '.join(self.deps1)
            
    @property
    def deps1(self):
        return self.n['deps1']
    
    @property
    def deps2(self):
        return self.n.get('deps2', [])
    
    @property
    def cmd(self):
        return self.n.get('cmd', [])

    async def run_cmd(self):
        return 0

    
class Item(ItemBase):
    def __init__(self, n, p):
        ItemBase.__init__(self, n)

        assert self.cmd
        
        self.p = p
        self.path = list(self.iter_deps())
        self.shell = self.find_shell()
        assert self.shell
        self.env = self.prepare_env()
        
    @property
    def build_results(self):
        return self.p.build_results
        
    @property
    def resolve_path(self):
        return self.p.resolve_path

    @property
    def shell_vars(self):
        return self.p.shell_vars
        
    def prepare_env(self):
        return dict(y.itertools.chain({'OUTER_SHELL': self.shell}.items(), y.fix_shell_vars(self.shell_vars)))
        
    def find_tool(self, tool):
        if tool[0] == '/':
            return tool

        return y.find_tool_cached(tool, self.path)

    def iter_deps(self):
        for d in self.deps2:
            yield y.os.path.join(y.os.path.dirname(self.resolve_path(d)), 'bin')

        yield from y.os.environ['PATH'].split(':')
            
    def find_shell(self):
        if '$YSHELL' in self.shell_vars:
            shell = self.find_tool(self.shell_vars['$YSHELL'])

            if shell:
                return shell
            
            raise Exception('can not find ' + self.shell_vars['$YSHELL'])
            
        return self.find_tool('dash') or self.find_tool('yash') or self.find_tool('sh') or self.find_tool('bash')

    def build_cmd(self):
        env = self.env
        
        def iter_cmd():
            yield 'set -e'
            yield 'set +x'
                
            for k in sorted(env, key=lambda x: -len(x)):
                yield 'export {k}={v}'.format(k=k, v=env[k])
                    
            yield 'export PATH="{runtime}:$PATH"'.format(runtime=y.build_scripts_dir())
            yield 'mainfun() {'

            for l in self.cmd:
                yield l
                    
            yield '}'
            yield 'mainfun ' + ' '.join(y.itertools.chain(self.deps1, self.deps2))
                
        input = '\n'.join(iter_cmd()) + '\n'
        input = input.replace('$(SHELL)', '$YSHELL')

        return input

    def check_results(self):
        for x in self.deps1:
            x = self.resolve_path(x)

            try:
                assert os.path.isfile(x)
            except Exception:
                raise Exception(x + ' not exists')

    async def run_cmd(self):
        sp = y.subprocess
        out = []
        retcode = 0
        input = self.build_cmd()
        
        try:
            p = sp.Popen([self.shell, '-s'], stdout=sp.PIPE, stderr=sp.STDOUT, stdin=sp.PIPE, shell=False, env=self.env)
            res, _ = p.communicate(input=input.encode('utf-8'))
            retcode = p.wait()
            res = res.decode('utf-8')
            res = res.strip()
            
            if not res:
                res = y.build_run_sh(self.n)

            # TODO
            if self.p.targets[0] == 'workspace':
                pass
            else:
                self.check_results()
        except sp.CalledProcessError as e:
            out.append(e.output)
            retcode = e.returncode
        except Exception:
            out.append(y.format_tbx())
            retcode = -1

        res = '\n'.join(y.super_decode(o.strip()) for o in out)

        self.build_out(res, retcode, input)

        return retcode

    def build_out(self, res, retcode, input):
        target = self.my_name
        
        msg = {
            'text': res,
            'command': input,
            'target': target,
        }
            
        if retcode:
            msg.update({
                'message': 'target {g}' + target + '{} failed, with retcode ' + str(retcode),
                'retcode': retcode,
                'target': target,
                'status': 'faulure'
            })
        else:
            msg.update({
                'message': 'target {g}' + target + '{} complete',
                'target': target,
            })

        self.build_results(msg)

        
async def run_par_build(ctl, lst, shell_vars, targets, threads):
    print lst
    b = Builder(ctl, lst, shell_vars, targets, threads)
    
    return await b.run()
