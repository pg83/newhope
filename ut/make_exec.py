@y.singleton
def is_debug():
    return 'debug' in y.config.get('make', '')


def run_makefile(mk, targets, threads, pre_run=[]):
    y.cheet(mk)

    if pre_run:
        run_par_build(mk.select_targets(pre_run), 1, False)

    if targets:
        mk = mk.select_targets(targets)

    return run_par_build(mk, threads, True)


def wrap_gen(func):
    def wrapper(inq):
        for x in func(inq):
            yield x

    return wrapper


def CHANNEL(data):
    return y.DATA(tags=['mk:channel'], data=data)


class Builder(object):
    def __init__(self, mk, threads, check):
        self.check = check
        self.mk = mk
        self.threads = threads
        self.lst = [item_factory(x, self, n) for n, x in enumerate(mk.lst)]

        by_dep = {}

        for x in self.lst:
            for d in x.deps1:
                by_dep[d] = x

        for k in by_dep.keys():
            self.resolve_path(k)

        self.by_dep = by_dep

    @property
    def shell_vars(self):
        return self.mk.flags

    @y.cached_method
    def resolve_path(self, d):
        return y.subst_vars(self.mk.strings[d], self.shell_vars)

    def runner(self, inq):
        yield y.EOP(y.ACCEPT('mk:build', 'mk:channel'), y.PROVIDES('mk:ready'))

        for el in inq:
            el = el.data.data

            is_debug() and y.debug('got', str(el))

            if el.get('action', '') == 'finish':
                yield y.FIN()

                return

            if (item := el.pop('item', None)) is not None:
                is_debug() and y.debug('run cmd', item)
                retcode = item.run_cmd()
                is_debug() and y.debug('done run cmd', item, retcode)

                if retcode:
                    yield CHANNEL({'action': 'finish', 'status': 'failure'})
                    yield y.FIN()

                    return

                if item.my_name == '_all':
                    yield CHANNEL({'action': 'finish', 'status': 'success'})
                    yield y.FIN()

                    return

                yield y.EOP(y.ELEM({'ready': item}))
            else:
                yield y.EOP()

        assert False

    def producer(self, inq):
        def iter_data():
            yield from self.lst

            lstl = len(self.lst)
            deps = sum([x.deps1 for x in self.lst], [])

            class ItemAll(object):
                @property
                def n(self):
                    return {'deps1': self.deps1, 'deps2': self.deps2, 'cmd': []}

                @property
                def my_name(self):
                    return '_all'

                @property
                def deps1(self):
                    return [self.num]

                @property
                def deps2(self):
                    return deps

                @property
                def num(self):
                    return lstl + 100000

                def run_cmd(self):
                    y.build_results({
                        'status': 'fini',
                        'message': 'build complete',
                        'target': self.my_name,
                    })

                    return 0

            yield ItemAll()

        def next_el():
            is_debug() and y.debug('wait next el')

            for el in inq:
                el = el.data.data
                is_debug() and y.debug('got', el)
                return el

        rq, wq = y.make_engine(iter_data(), lambda x: x.deps1[0], dep_list=lambda x: sorted(frozenset(x.deps2)))
        by_n = {}
        complete = set()

        yield y.EOP(y.ACCEPT('mk:ready', 'mk:channel'), y.PROVIDES('mk:build'))

        def fmt_in_fly(data):
            return '(' + ', '.join([x['x'].my_name for x in data.values()]) + ')'

        while True:
            for i, el in enumerate(rq()):
                item = el['x']
                by_n[item.num] = el

                is_debug() and y.debug('yield ready', y.pd(item), 'in fly', fmt_in_fly(by_n))

                yield y.ELEM({'item': item})
                yield y.EOP()

            yield y.EOP()

            el = next_el()

            if el.get('action', '') == 'finish':
                yield y.FIN()

                return

            if (item := el.get('ready')) is not None:
                key = y.burn(item.n)
                assert key not in complete
                complete.add(key)
                wq(by_n.pop(item.num)['i'])
                is_debug() and y.debug('got complete', item, 'in fly', fmt_in_fly(by_n))

        assert False

    def run(self):
        p = y.PubSubLoop()

        def iter_workers():
            yield y.make_name(wrap_gen(self.producer), 'producer_0')

            for i in range(0, self.threads):
                yield y.make_name(wrap_gen(self.runner), 'runner_' + str(i))

        return p.run(thrs=list(iter_workers()))


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
    def check(self):
        return self.p.check

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

    def run_cmd(self):
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

    def check_done(self):
        try:
            self.check_results()

            return True
        except Exception:
            pass

        return False

    def run_cmd(self):
        target = self.my_name

        if self.check_done():
            y.build_results({
                'message': 'use cached {target}',
                'status': 'done',
                'target': target,
            })

            return 0

        y.build_results({
            'message': 'starting {target}',
            'status': 'init',
            'target': target,
        })

        retcode, res, input = self.run_cmd_0()

        def iter_lines():
            bdir = ''

            for l in res.strip().split('\n'):
                if 'export ' in l:
                    #yield l

                    if 'BDIR' in l:
                        bdir = l.split('=')[1]

            if bdir:
                yield '{br}./cli debug ' + bdir + '{}'

        msg = {
            'output': '\n'.join(iter_lines()),
            'command': input,
            'target': target,
        }

        if retcode:
            msg.update({
                'message': 'target {target} failed',
                'status': 'fail',
                'retcode': retcode,
            })
        else:
            msg.update({
                'message': 'target {target} complete',
                'status': 'done',
            })

        y.build_results(msg)

        if retcode:
            y.shut_down(5, last_msg='{br}target ' + target + ' failed, exiting now{}\n')

    def run_cmd_0(self):
        sp = y.subprocess
        out = []
        retcode = 0
        input = self.build_cmd()

        try:
            env = y.dc(self.env)
            naked = False

            def fun():
                input_bin = input.encode('utf-8')
                env['RUNSH'] = y.base64.b64encode(input_bin)
                env['REDIRECT'] = "yes"

                if naked:
                    stdo = y.sys.__stderr__
                    stde = y.sys.__stderr__
                else:
                    stdo = sp.PIPE
                    stde = sp.STDOUT

                p = sp.Popen([self.shell, '-s'], stdout=stdo, stderr=stde, stdin=sp.PIPE, shell=False, env=env)
                res, _ = p.communicate(input=input_bin)
                res = res or ''
                retcode = p.wait()

                return (res, retcode)

            res, retcode = fun()

            res = res.strip()

            if not res:
                res = y.build_run_sh(self.n)

            out.append(res)

            if retcode == 0:
                if self.check:
                    self.check_results()
        except sp.CalledProcessError as e:
            out.append(e.output)
            retcode = e.returncode
        except Exception:
            out.append(y.format_tbx())
            retcode = -1

        return retcode, '\n'.join(y.super_decode(o.strip()) for o in out), input


def run_par_build(mk, threads, check):
    y.info('{br}start build{}')

    try:
        return Builder(mk, threads, check).run()
    finally:
        y.info('{br}end build{}')
