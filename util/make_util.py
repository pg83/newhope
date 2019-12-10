def new_cmd():
    return {
        'cmd': [],
    }


@y.singleton
def good_sym():
    a = [chr(ord('a') + x) for x in range(0, 26)]
    b = [x.upper() for x in a]
    c = [i for i in range(0, 10)]

    return frozenset(a + b + c)


def sanitize_string(s):
    gs = good_sym()
    
    def iter_good():
        for c in s:
            if c in gs:
                yield c
            else:
                yield '_'

    return ''.join(iter_good())


def hash(x):
    return y.burn([sorted(x['deps1']), sorted(x['deps2']), x['cmd']])


def get_only_our_targets(lst, targets):
    by_link = {}
    
    for n, l in enumerate(lst):
        for d in l['deps1']:
            by_link[d] = n

    v = set()

    def visit(n):
        if n is None:
            return
        
        if n in v:
            return

        yield n

        v.add(n)

        for l in [by_link.get(d, None) for d in lst[n]['deps2']]:
            for x in visit(l):
                yield x

    def iter():
        for t in targets:
            yield from visit(by_link[t])
                
    return [lst[x] for x in sorted(frozenset(iter()))]
    

def subst_vars(d, shell_vars):
    while '$' in d:
        for k, v in shell_vars.items():
            d = d.replace(k, v)
            
    return d


def remove_d(k):
    if k[0] == '$':
        return k[1:]
                
    return k


def super_decode(s):
    try:
        return s.decode('utf-8')
    except Exception:
        return s
            

def fix_shell_vars(shell_vars):
    return [(remove_d(k), v) for k, v in shell_vars.items()]


@y.cached()
def cached_file_list(where):
    try:
        return frozenset([x for x in y.os.listdir(where)])
    except FileNotFoundError:
        return frozenset()

    
@y.cached()
def find_tool_cached(tool, path):
    for p in path:
        if tool in cached_file_list(p):
            return p + '/' + tool


async def parse_makefile(data):
    lst = []
    prev = None
    cprint = y.xprint_white
    parse_flags = True
    shell_args = {}
    
    for line_no, l in enumerate(data.split('\n')):
        if parse_flags:
            if '=' in l:
                pos = l.find('=')
                key = l[:pos].strip()
                val = l[pos + 1:].strip()
                shell_args['$' + key] = val

                continue
            else:
                print(shell_args, file=y.sys.stderr)
                parse_flags = False
        
        p = l.find('##')

        if p > 5:
            l = l[:p]

        ls = l.strip()

        if not ls:
            continue

        if ls.startswith('#'):
            continue

        if l[0] != '\t':
            if prev:
                lst.append(prev)

            prev = new_cmd()

            def iter_deps(ll):
                for l in ll.strip().split(' '):
                    l = l.strip()

                    if l:
                        yield l

            try:
                a, b = ls.split(':')
            except Exception as e:
                y.xprint_r(ls, line_no, e)

                raise

            prev['deps1'] = list(iter_deps(a))
            prev['deps2'] = list(iter_deps(b))
        else:
            prev['cmd'].append(l[1:].rstrip())

    if prev:
        lst.append(prev)
        
    return {'lst': lst, 'flags': shell_args}


async def cheet(mk):
    @y.singleton
    def placeholder():
        bsp = mk.bsp()

        def build_scripts_path():
            return bsp

        def build_scripts_dir():
            return y.os.path.dirname(bsp)

        l = locals()
        
        @y.lookup
        def look(name):
            return l[name]

    try:
        y.build_scripts_dir()
    except AttributeError:
        placeholder()
        y.build_scripts_dir()


async def select_targets(lst, targets):
    return get_only_our_targets(lst, targets)


def build_run_sh(n):
    def iter_run_sh():
        yield '{br}running {bw}[cname]'
        yield '{by} run.sh:'

        for l in n['cmd']:
            yield '  ' + l

    return '\n'.join(iter_run_sh())


class MakeArgs(dict):
    def __init__(self):
        self.__dict__ = self


class MakeFile(object):
    async def init(self, lst):
        try:
            return self.init_from_dict(y.decode_prof(lst))
        except Exception as e1:
            exc1 = e1
        
        try:
            return self.init_from_parsed(await parse_makefile(lst))
        except Exception as e2:
            exc2 = e2
            
        try:
            return self.init_from_parsed(await parse_makefile(lst.decode('utf-8')))
        except Exception as e2:
            exc2 = e2

        raise Exception('can not parse makefile: ' + str(exc1) + ', ' + str(exc2))

    def init_from_dict(self, d):
        self.lst = d['d']
        self.flags = d['f']
        self.strings = d['s']
        self.str_to_num = dict((x, i) for i, x in enumerate(self.strings))

        return self

    def clone(self):
        mk = MakeFile()

        mk.lst = self.lst
        mk.flags = self.flags
        mk.strings = self.strings
        mk.str_to_num = self.str_to_num

        return mk
        
    def init_from_parsed(self, parsed):
        lst = parsed['lst']

        self.flags = parsed['flags']
        self.strings = []
        self.str_to_num = {}

        def iter_items():
            all_deps_1 = []
            all_deps_2 = []
            
            for l in lst:
                n = dict((k, self.cvt(l, k)) for k in ('deps1', 'deps2', 'cmd'))

                all_deps_1.extend(n['deps1'])
                all_deps_2.extend(n['deps2'])
                
                yield n

            for d in sorted(frozenset(all_deps_2) - frozenset(all_deps_1)):
                yield {'deps1': [d], 'deps2': [], 'cmd': []}
                
            if 'all' not in all_deps_1:
                yield {'deps1': self.lst_to_nums(['all']), 'deps2': all_deps_1, 'cmd': []}
            
        self.lst = list(iter_items())

        return self
        
    def cvt(self, l, name):
        return self.lst_to_nums(l.get(name, []))
        
    def bsp(self):
        return self.strings[self.lst[0]['deps1'][0]]

    def stn(self, s):
        if s in self.str_to_num:
            return self.str_to_num[s]

        k = len(self.strings)
        
        self.strings.append(s)
        self.str_to_num[s] = k

        return k
    
    def lst_to_nums(self, l):
        return [self.stn(s) for s in l]

    def nums_to_str(self, l):
        return [self.strings[s] for s in l]

    async def select_targets(self, targets):
        mk = MakeFile()

        lst = await select_targets(self.lst, self.lst_to_nums(sorted(targets)))
        lst = [self.restore_node(x) for x in lst]

        mk.init_from_parsed({'lst': lst, 'flags': y.deep_copy(self.flags)})
        
        return mk

    def restore_node(self, n):
        return dict((k, self.nums_to_str(n[k])) for k in ('deps1', 'deps2', 'cmd'))

    async def build(self, shell_vars, args):
        mk = self.clone()

        mk.flags = y.deep_copy(mk.flags)
        mk.flags.update(shell_vars)
        
        return await y.run_make_0(mk, args)

    async def build_kw(self, shell_vars, **kwargs):
        args = MakeArgs()

        args.threads = kwargs.pop('threads', 1)
        args.targets = kwargs.pop('targets', ['all'])
        args.pre_run = kwargs.pop('pre_run', [])
        
        args.update(kwargs)

        return await self.build(shell_vars, args)

    
def dumps_mk(mk):
    return y.encode_prof({'d': mk.lst, 's': mk.strings, 'f': mk.flags})

    
def loads_mk(t):
    return MakeFile().init_from_dict(y.decode_prof(t))


async def open_mk_file(path, gen=None):
    if gen and path == 'gen':
        return await gen()
    
    if path == '-':
        data = await y.offload(y.sys.stdin.read)
    elif path:
        with open(path, 'r') as f:
            data = await y.offload(f.buffer.read)
    else:
        data = await y.offload(y.sys.stdin.read)

    mk = MakeFile()

    await mk.init(data)

    return mk
