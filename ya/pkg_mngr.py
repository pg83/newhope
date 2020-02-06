class InstPropertyDB(object):
    def __init__(self, db):
        self.db = db

        if 'inst' not in db:
            db['inst'] = []

        if 'idx' not in db:
            db['idx'] = []

    def inst(self):
        return self.db['inst']

    def set_inst(self, v):
        self.db['inst'] = v

    def target(self):
        return self.db['target']

    def set_target(self, target):
        self.db['target'] = target

    def add_index_file(self, f):
        self.db['idx'].append(f)

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
        for f in self.get_index_files():
            y.info('will fetch', f)

            for x in y.decode_prof(y.fetch_data(f)):
                x['index'] = f
                yield x

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
                    by_time.append(i)

        return sorted(by_time, key=lambda x: x['ts'])

    def pkg_list(self, pkgs):
        pkgs = self.resolve_groups(pkgs)
        dd = {}

        for l in self.search_pkgs(pkgs):
            p1, p2 = l['path'].split('-v5')
            dd[p1] = l

        diff = frozenset([x.split('-')[0] for x in pkgs]) - frozenset([x.split('-')[0] for x in dd.keys()])

        if diff:
            raise Exception('not all packages found ' + str(diff))

        return list(dd.values())

    @y.contextlib.contextmanager
    def open_db(self):
        with y.open_simple_db(y.os.path.join(self.path, 'etc', 'upm', 'sys.db')) as db:
            yield InstPropertyDB(db)

    def install(self, pkgs):
        def do(inst):
            return y.uniq_list_x(inst + pkgs)

        self.modify(do)

    def delete(self, pkgs):
        def do(inst):
            pkgs = frozenset(pkgs)

            for i in inst:
                if i not in pkgs:
                    yield i

        self.modify(do)

    def modify(self, func):
        try:
            with self.open_db() as db:
                y.info('write next state')
                db.set_inst(func(list(db.inst())))
                self.apply_db(db)
        except Exception as e:
            try:
                y.error('in install: ', e)
                self.revert_changes()
            finally:
                raise e

    def revert_changes(self):
        with self.open_db() as db:
            self.apply_db(db)

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

            y.os.system('cd ' + ppath_tmp  + ' && tar -xf ' + path + ' && mv ' + ppath_tmp + ' ' + ppath)

        ap = self.all_packs()

        with open(self.pkg_dir() + '/path', 'w') as f:
            f.write('export PATH=' + ':'.join([('/pkg/' + x + '/bin') for x in ap]))

        for x in frozenset(ap) - frozenset([x['path'] for x in lst]):
            y.warning('remove stale package', x)
            y.shutil.rmtree(y.os.path.join(self.pkg_dir(), x))


    def fetch_package(self, pkg):
        y.info('will fetch package{br}', pkg['path'], '{}')

        return y.fetch_data(y.os.path.dirname(pkg['index']) + '/' + pkg['path'])

    def init_place(self):
        try:
            y.os.makedirs(self.path)
        except OSError:
            pass

        with self.open_db() as db:
            db.set_target(self.info)
            db.add_index_file('http://index.samokhvalov.xyz/index')

        base = self.pkg_list(['base'])[0]

        y.os.chdir(self.path)

        with open(base['path'] + '.tar', 'wb') as f:
            f.write(y.decode_prof(self.fetch_package(base)))
            y.os.system('tar -xf *.tar && rm -rf log base* build')
