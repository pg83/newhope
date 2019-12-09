@y.singleton
def is_debug():
    return 'debug' in y.config.get('make', '')


async def run_makefile(mk, shell_vars, targets, threads, pre_run=[]):
    async def run_build_2(ctl):
        await y.cheet(mk)
    
        if pre_run:
            await run_par_build(ctl, await mk.select_targets(pre_run), shell_vars, pre_run, 1)

        return await run_par_build(ctl, await mk.select_targets(targets), shell_vars, targets, threads)

    return await y.spawn(run_build_2)


def wrap_gen(func):
    async def wrapper(ctl, inq):
        async for x in func(ctl, inq):
            yield x

    return wrapper


def CHANNEL(data):
    return y.DATA(tags=['mk:channel'], data=data)

        
class Builder(object):
    def __init__(self, ctl, mk, shell_vars, targets, threads):
        self.mk = mk
        self.threads = threads
        self.ctl = ctl
        self.shell_vars = shell_vars
        self.targets = targets
        self.lst = [item_factory(x, self, n) for n, x in enumerate(mk.lst)]
        
        by_dep = {}

        for x in self.lst:
            for d in x.deps1:
                by_dep[d] = x

        for k in by_dep.keys():
            self.resolve_path(k)

        self.by_dep = by_dep
        
    @y.cached_method
    def resolve_path(self, d):
        return y.subst_vars(self.mk.strings[d], self.shell_vars)

    async def runner(self, ctl, inq):
        yield y.EOP(y.ACCEPT('mk:build', 'mk:channel'), y.PROVIDES('mk:ready'))
        
        async for el in inq:
            el = el.data.data
            
            is_debug() and y.debug('got', str(el))

            if el.get('action', '') == 'finish':
                yield y.FIN()

                return

            if (item := el.pop('item', None)) is not None:
                retcode = await item.run_cmd(ctl)

                if retcode:
                    yield CHANNEL({'action': 'finish', 'status': 'failure'})
                    yield y.FIN()

                    return
                    
                if item.my_name == 'all':
                    yield CHANNEL({'action': 'finish', 'status': 'success'})
                    yield y.FIN()

                    return

                yield y.EOP(y.ELEM({'ready': item}))
            else:
                yield y.EOP()
                
        assert False

    async def producer(self, ctl, inq):
        rq, wq = y.make_engine(self.lst, lambda x: x.deps1[0], dep_list=lambda x: sorted(frozenset(x.deps2)))
        by_n = {}
        complete = set()
        
        yield y.EOP(y.ACCEPT('mk:ready', 'mk:channel'), y.PROVIDES('mk:build'))

        while True:
            for i, el in enumerate(rq()):
                item = el['x']
                by_n[item.num] = el
                
                is_debug() and y.debug('yield ready', y.pretty_dumps(item))

                yield y.ELEM({'item': item})

            yield y.EOP()

            is_debug() and y.debug('wait for complete')

            async for el in inq:
                el = el.data.data

                if el.get('action', '') == 'finish':
                    yield y.FIN()

                    return
                
                if (item := el.get('ready')) is not None:
                    key = y.burn(item.n)
                    assert key not in complete
                    complete.add(key)
                    is_debug() and y.debug('got complete', item)
                    wq(by_n[item.num]['i'])
                    
                    break

        assert False
    
    async def run(self):
        p = y.PubSubLoop(self.ctl)
        
        def iter_workers():
            yield y.set_name(wrap_gen(self.producer), 'producer_0')
            
            for i in range(0, self.threads):
                yield y.set_name(wrap_gen(self.runner), 'runner_' + str(i))

        return await p.run(coro=list(iter_workers()))

    def on_build_status(self, fail):
        if fail:
            y.build_results({'message': 'done', 'status': 'ok'})
        else:
            y.build_results({'message': 'fail', 'status': 'failure'})


def item_factory(n, p, i):
    if n.get('cmd'):
        return Item(n, p, i)

    return ItemBase(n, p, i)
            

class ItemBase(object):
    def __init__(self, n, p, i):
        self.n = n
        self.p = p
        self.i = i
        
    def __str__(self):
        return y.json.dumps(self.__json__(), sort_keys=True)
        
    def __json__(self):
        return {
            'num': self.num,
            'cmd': self.cmd,
            'output': self.deps1[0],
            'inputs': self.deps2,
            'id': id(self),
        }

    @property
    def num(self):
        return self.i
    
    @property
    def my_name(self):
        return ', '.join(self.str_deps1)
            
    @property
    def deps1(self):
        return self.n['deps1']
    
    @property
    def str_deps1(self):
        return self.p.mk.nums_to_str(self.deps1)
    
    @property
    def deps2(self):
        return self.n.get('deps2', [])
    
    @property
    def str_deps2(self):
        return self.p.mk.nums_to_str(self.deps2)
    
    @property
    def cmd(self):
        return self.n.get('cmd', [])
    
    @property
    def str_cmd(self):
        return self.p.mk.nums_to_str(self.cmd)
        
    @property
    def resolve_path(self):
        return self.p.resolve_path

    async def run_cmd(self, ctl):
        y.build_results({
            'message': 'done',
            'target': self.my_name,
        })
        
        return 0

    
class Item(ItemBase):
    def __init__(self, n, p, i):
        ItemBase.__init__(self, n, p, i)

        assert self.cmd
        
        self.path = list(self.iter_search_path())
        self.shell = self.find_shell()
        assert self.shell
        self.env = self.prepare_env()

    def __json__(self):
        res = ItemBase.__json__(self)

        res.update({
            'shell': self.shell,
            'env': self.env,
        })

        return res
    
    @property
    def shell_vars(self):
        return self.p.shell_vars
        
    def prepare_env(self):
        return dict(y.itertools.chain({'OUTER_SHELL': self.shell}.items(), y.fix_shell_vars(self.shell_vars)))
        
    def find_tool(self, tool):
        if tool[0] == '/':
            return tool

        return y.find_tool_cached(tool, self.path)

    def iter_search_path(self):
        for d in self.deps2:
            yield y.os.path.join(y.os.path.dirname(self.resolve_path(d)), 'bin')

        yield from y.os.environ['PATH'].split(':')
            
    def find_shell(self):
        if '$YSHELL' in self.shell_vars:
            shell = self.find_tool(self.shell_vars['$YSHELL'])

            if shell:
                return shell
            
            raise Exception('can not find ' + self.shell_vars['$YSHELL'])
            
        return self.find_tool('dash') or self.find_tool('yash') or self.find_tool('bash') or self.find_tool('sh')

    def build_cmd(self):
        env = self.env
        
        def iter_cmd():
            yield 'set -e'
            yield 'set -x'
            
            for k in sorted(env, key=lambda x: -len(x)):
                yield 'export {k}={v}'.format(k=k, v=env[k])

            yield 'mainfun() {'
            
            for l in self.str_cmd:
                yield l
                    
            yield '}'
            yield 'mainfun ' + ' '.join(y.itertools.chain(self.str_deps1, self.str_deps2))
                
        input = '\n'.join(iter_cmd()) + '\n'
        input = input.replace('$(SHELL)', '$YSHELL')

        return input

    def check_results(self):
        for x in self.deps1:
            x = self.resolve_path(x)

            try:
                assert y.os.path.isfile(x)
            except Exception as e:
                raise Exception(x + ' not exists: ' + str(e))

    async def run_cmd(self, ctl):
        try:
            self.check_results()
            all_done = True
        except Exception:
            all_done = False

        if all_done:
            y.build_results({
                'message': 'done',
                'target': self.my_name,
            })

            return 0

        y.build_results({
            'message': 'init',
            'target': self.my_name,
        })
        
        sp = y.subprocess
        out = []
        retcode = 0
        input = self.build_cmd()
        
        try:
            env = y.deep_copy(self.env)
            
            def fun():
                input_bin = input.encode('utf-8')
                env['RUNSH'] = y.base64.b64encode(input_bin)
                p = sp.Popen([self.shell, '-s'], stdout=sp.PIPE, stderr=sp.STDOUT, stdin=sp.PIPE, shell=False, env=env)
                res, _ = p.communicate(input=input_bin)
                retcode = p.wait()

                return (res, retcode)

            res, retcode = await ctl.loop.offload(y.set_name(fun, 'fun_' + y.sanitize_string(self.my_name)))
            
            res = res.decode('utf-8')
            res = res.strip()
            
            if not res:
                res = y.build_run_sh(self.n)

            out.append(res)

            if retcode == 0:
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

        if retcode:
            print res, input
        
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
                'message': 'fail',
                'retcode': retcode,
                'target': target,
                'status': 'faulure'
            })
        else:
            msg.update({
                'message': 'done',
                'target': target,
            })

        y.build_results(msg)

        
async def run_par_build(ctl, mk, shell_vars, targets, threads):
    build = ', '.join(targets)

    y.info('{r}start build of', build, '{}')

    try:
        async def run_par_build_1(ctl):
            b = Builder(ctl, mk, shell_vars, targets, threads)

            return await b.run()

        return await ctl.spawn(run_par_build_1)
    finally:
        y.info('{r}end build of', build, '{}')
