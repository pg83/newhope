def new_cmd():
    return {
        'cmd': [],
    }


def hash(x):
    return y.burn([sorted(x['deps1']), sorted(x['deps2']), x['cmd']])


def get_only_our_targets(lst, targets):
    by_link = {}

    for l in lst:
        for d in l['deps1']:
            by_link[d] = l['n']

    v = set()

    def visit(n):
        if n in v:
            return

        yield n

        v.add(n)

        for l in [by_link[d] for d in lst[n]['deps2']]:
            for x in visit(l):
                yield x

    def iter():
        for t in targets:
            for x in visit(by_link[t]):
                yield x
                
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
    print 'x'
    lst = []
    prev = None
    cprint = y.xprint_white

    for line_no, l in enumerate(data.split('\n')):
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
        
    return lst


async def cheet(lst):
    @y.singleton
    def placeholder():
        bsp = lst[0]['deps1'][0]
            
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
    for i, l in enumerate(lst):
        l['n'] = i

    lst = get_only_our_targets(lst, targets)

    for i, l in enumerate(lst):
        l['n'] = i

    return lst


def build_run_sh(n):
    def iter_run_sh():
        yield '{r}running {w}[cname]'
        yield '{y} run.sh:'

        for l in n['cmd']:
            yield '  ' + l

    return '\n'.join(iter_run_sh())
