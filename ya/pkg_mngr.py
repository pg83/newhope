class Fetcher(object):
    def fetch_index(self):
        for x in y.decode_prof(self.fetch('index')):
            x['index'] = self

            yield x


class HTTPFetcher(Fetcher):
    def __init__(self, root):
        self._root = root
        
    def fetch(self, path):
        p = y.os.path.join(self._root, path)
        
        y.info('will fetch{bg}', p, '{}')
        
        return y.fetch_data(p)


class LocalFetcher(Fetcher):
    def __init__(self, root):
        self._root = root

    def fetch(self, path):
        p = y.os.path.join(self._root, path)

        y.info('will fetch {br}', p, '{}')
        
        with open(p, 'wb') as f:
            return f.read()


def get_fetcher(path):
    if path.startswith('http'):
        return HTTPFetcher(path)

    return LocalFetcher(path)
        

class InstPropertyDB(object):
    def __init__(self, db):
        self.db = db
        self.state = y.marshal.dumps(self.db)

        if 'inst' not in db:
            db['inst'] = []

        if 'idx' not in db:
            db['idx'] = []

        self.add_index_file([])
            
    def restore_state(self):
        self.db = y.marshal.loads(self.state)
            
    def inst(self):
        return self.db['inst']

    def set_inst(self, v):
        self.db['inst'] = v

    def target(self):
        return self.db['target']

    def set_target(self, target):
        self.db['target'] = target

    def add_index_file(self, f):
        self.db['idx'] = list(reversed(y.uniq_list_x(reversed(self.db['idx'] + f))))

    def index_files(self):
        return self.db['idx']


def find_file(pattern):
    p = y.os.path.abspath(y.os.getcwd())

    def do():
        n = '/'

        for x in p.split('/') + ['']:
            probe = y.os.path.join(n, pattern)

            if y.os.path.isfile(probe):
                yield probe

            n = y.os.path.join(n, x)

    data = list(do())

    if not data:
        raise Exception('no upm target in current stack')

    return data[-1]


class PkgMngr(object):
    def __init__(self, info=None, path=None):
        trf = 'etc/upm/sys.db'

        if not info:
            try:
                if path:
                    tgpath = y.os.path.join(path, trf)
                else:
                    tgpath = find_file(trf)

                self.path = y.os.path.abspath(tgpath)[:-len(trf)]

                with self.open_db() as db:
                    info = db.target()

                path = self.path
            except OSError:
                pass

        if not info:
            raise Exception("you should provide target platform")

        self.path = path
        self.info = info

    def subst_packs(self, p1, p2):
        return frozenset(self.pkg_unv_name(x) for x in p1) - frozenset(self.pkg_unv_name(x) for x in p2)

    def get_dir(self, *args):
        return y.os.path.join(self.path, *args)

    def etc_dir(self):
        return self.get_dir('etc')

    def upm_dir(self):
        return self.etc_dir() + '/upm'

    def get_dir_simple(self, args):
        return (self.path + args).replace('//', '/')

    def pkg_cache_dir(self):
        return self.pkg_dir() + '/cache'

    def pkg_dir(self):
        return self.get_dir('pkg')

    def all_packs(self):
        def do():
            for x, _ in self.list_dir(self.pkg_dir()):
                if '-v5' in x:
                    yield x

        return list(do())

    def list_dir(self, path):
        where = y.os.path.join(self.path, path)

        if not y.os.path.isdir(where):
            y.warning('not a directory', where)

            return

        for x in y.os.listdir(where):
            yield x, y.os.path.join(x, where)

    def get_index_files_0(self):
        with self.open_db() as db:
            yield from db.index_files()

    def get_index_files(self):
        return list(self.get_index_files_0())

    def collect_indices_0(self):
        cnt = 0
        
        for f in self.get_index_files():
            try:
                yield from get_fetcher(f).fetch_index()
                cnt += 1
            except Exception as e:
                y.warning('skip source', f)

        if not cnt:
            raise Exception('all sources dead')
                
    def collect_indices(self):
        return list(self.collect_indices_0())

    def resolve_groups_0(self, pkgs):
        for g in pkgs:
            if g[0] == '@':
                yield from self.resolve_groups_0(y.distr_by_name(g[1:]))
            else:
                yield g

    def resolve_groups(self, pkgs):
        return y.uniq_list_x(self.resolve_groups_0(pkgs))

    def search_pkgs(self, pkgs, list_all=False):
        def flt_index():
            for i in self.collect_indices():
                if list_all:
                    yield i
                elif i['path'].startswith('tow'):
                    y.debug('skip', i['path'], 'skip dev path')
                elif self.info not in i['path']:
                    y.debug('skip', i['path'], self.info)
                else:
                    yield i

        index = list(flt_index())
        by_time = []

        for i in index:
            for p in pkgs:
                if i['path'].startswith(p + '-' + self.info):
                    i['join'] = p
                    by_time.append(i)

        return sorted(by_time, key=lambda x: x['ts'])

    def pkg_unv_name(self, full_name):
        return full_name.split('-' + self.info)[0]

    def pkg_list(self, pkgs):
        pkgs = self.resolve_groups(pkgs)
        dd = {}
        by_num = dict((x, i) for i, x in enumerate(pkgs))

        for l in self.search_pkgs(pkgs):
            p1, p2 = l['path'].split('-v5')
            dd[p1] = l

        diff = self.subst_packs(pkgs, dd.keys())

        if diff:
            raise Exception('not all packages found ' + str(diff))

        return sorted(dd.values(), key=lambda x: by_num[x['join']])

    @y.contextlib.contextmanager
    def open_db(self):
        with y.open_simple_db(y.os.path.join(self.path, 'etc', 'upm', 'sys.db')) as db:
            yield InstPropertyDB(db)

    def install(self, pkgs):
        def do(inst):
            return y.uniq_list_x(inst + pkgs)

        self.modify(do)

    def delete_x(self, pkgs):
        pkgs = frozenset(pkgs)

        def do(inst):
            for i in inst:
                if i not in pkgs:
                    yield i

        self.modify(do)

    def modify(self, func):
        try:
            with self.open_db() as db:
                y.info('write next state')
                db.set_inst(list(func(db.inst())))
                self.apply_db(db)
        except Exception as e:
            try:
                db.restore_state()
            finally:
                raise e
            
    def apply_db(self, db):
        y.info('apply actual changes')
        self.actual_install(db.inst())

    def actual_install(self, pkgs):
        lst = self.pkg_list(pkgs)

        for p in lst:
            ppath = self.pkg_dir() + '/' + p['path']

            if y.os.path.isdir(ppath):
                y.info('skip', ppath)

                continue

            data = self.fetch_package(p)
            path = y.os.path.join(self.pkg_cache_dir(), p['path']) + '.tar'

            with open(path, 'wb') as f:
                f.write(y.decode_prof(data))

            ppath_tmp = self.pkg_dir() + '/.' + p['path']
            ppath = self.pkg_dir() + '/' + p['path']

            try:
                y.os.makedirs(ppath_tmp)
            except OSError:
                y.shutil.rmtree(ppath_tmp)
                y.os.makedirs(ppath_tmp)

            y.os.system('cd ' + ppath_tmp  + ' && tar -xf ' + path + ' && ./install && mv ' + ppath_tmp + ' ' + ppath)

        ap = self.all_packs()

        with open(self.pkg_dir() + '/profile', 'w') as f:
            f.write('export PATH=' + ':'.join([('/pkg/' + x + '/bin') for x in ap]))

        for x in self.subst_packs(ap, [x['path'] for x in lst]):
            y.warning('remove stale package', x)
            y.shutil.rmtree(y.os.path.join(self.pkg_dir(), x))


    def fetch_package(self, pkg):
        return pkg['index'].fetch(pkg['path'])

    def init_place(self):
        try:
            y.os.makedirs(self.path)
        except OSError:
            pass

        with self.open_db() as db:
            db.set_target(self.info)
            db.add_index_file(['http://index.samokhvalov.xyz'])

        base = self.pkg_list(['base'])[0]

        y.os.chdir(self.path)

        with open(base['path'] + '.tar', 'wb') as f:
            f.write(y.decode_prof(self.fetch_package(base)))
            y.os.system('tar -xf *.tar && rm -rf log base* build')

    def add_indexes(self, indexes):
        with self.open_db() as db:
            db.add_index_file(indexes)
            
