sp = y.subprocess
os = y.os


def untar_from_memory(tar, data, where):
    p = sp.Popen([tar, '-C', where, '-xf', '-'], shell=False, stderr=sp.STDOUT, stdout=sp.PIPE, stdin=sp.PIPE)
    out, _ = p.communicate(input=data)
    retcode = p.wait()

    if retcode == 0:
        return

    raise Exception('can not untar data: ' + out.decode('utf-8'))


def build_index(where):
    y.info('build index for{bb}', where, '{}')

    index = []

    for f in sorted(os.listdir(where)):
        if len(f) > 10:
            p = os.path.join(where, f)

            if '-tmp.' in f:
                continue

            if f.startswith('.'):
                continue

            index.append({'path': f, 'length': os.path.getsize(p), 'ts': int(1000000000 * os.path.getmtime(p))})

    return index


class Fetcher(object):
    @y.cached_method
    def fetch_index(self):
        for x in self.do_fetch_index():
            x['index'] = self

            yield x

    def fetch(self, name):
        assert name != 'index'

        return self.do_fetch(name)


def safe_symlink_0(fr, to):
    tmp_to = y.tmp_name(to)

    os.symlink(fr, tmp_to)
    os.rename(tmp_to, to)


def safe_symlink(fr, to):
    try:
        return safe_symlink_0(fr, to)
    except Exception:
        y.info('can not do symlink, will retry', str(e))
        y.time.sleep(1)

    return safe_symlink_0(fr, to)


class HTTPFetcher(Fetcher):
    def __init__(self, root):
        self._root = root

    def path(self, x):
        return os.path.join(self._root, x)

    def do_fetch_index(self):
        p = self.path('index')

        y.info('fetch index for{bb}', p, '{}')

        return y.decode_prof(y.fetch_data(p))

    def do_fetch(self, path):
        p = self.path(path)

        y.info('fetch{by}', p, '{}')

        return y.fetch_data(p)


class LocalFetcher(Fetcher):
    def __init__(self, root):
        self._root = root

    def do_fetch_index(self):
        return y.build_index(self._root)

    def do_fetch(self, path):
        p = os.path.join(self._root, path)

        y.info('fetch{bm}', p, '{}')

        with open(p, 'rb') as f:
            return f.read()


@y.cached
def get_fetcher(path):
    if path.startswith('http'):
        return HTTPFetcher(path)

    return LocalFetcher(path)


class ProgressBar(object):
    def __init__(self, m):
        self._m = m
        self._c = 0

    def next_str(self):
        self._c += 1

        return '{bw}{' + str(self._c) + ' of ' + str(self._m) + '}{}'


class InstPropertyDB(object):
    def __init__(self, db):
        self.db = db
        self.state = y.marshal.dumps(self.db)

        y.ensure_value('inst', db, [])
        y.ensure_value('idx', db, [])

        self.add_index_file([])

    def restore_state(self):
        y.warning('{br}restore db state cause prev errors{}')

        old = y.marshal.loads(self.state)

        self.db.clear()
        self.db.update(old)

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
    p = os.path.abspath(os.getcwd())

    def do():
        n = '/'

        for x in p.split('/') + ['']:
            probe = os.path.join(n, pattern)

            if os.path.isfile(probe):
                yield probe

            n = os.path.join(n, x)

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
                    tgpath = os.path.join(path, trf)
                else:
                    tgpath = find_file(trf)

                self.path = os.path.abspath(tgpath)[:-len(trf)]

                with self.open_db() as db:
                    info = db.target()

                path = self.path
            except OSError:
                pass

        if not info:
            raise Exception("you should provide target platform")

        self.path = path
        self.info = info

    def all_packs_dict(self):
        res = {}

        try:
            real_files = list(os.listdir(self.pkg_dir()))
        except FileNotFoundError:
            return {}

        for x in real_files:
            if '-v5' not in x:
                continue

            if '-tmp.' in x:
                continue

            name = self.pkg_unv_name(x)
            res[name] = x

        return res

    def any_of(self, pkgs):
        ap = self.all_packs_dict()

        for p in pkgs:
            if p in ap:
                return ap[p]

        raise AttributeError('no ' + str(pkgs) + 'found')

    def find_pkg_tar(self):
        lst = ['tar']
        full_lst = lst + [(x + '-run') for x in lst]
        tar = os.path.join(self.path, 'pkg', self.any_of(full_lst), 'bin', 'tar')

        if not os.path.isfile(tar):
            raise AttributeError(tars)

        return tar

    def untar_from_memory(self, data, where):
        try:
            os.makedirs(where)
        except OSError:
            pass

        try:
            untar_from_memory(self.find_pkg_tar(), data, where)
        except Exception as e:
            y.debug('fallback to python tarfile: ' + str(e))

            import io

            stream = io.BytesIO(data)
            y.tarfile.open(fileobj=stream, mode='r').extractall(where)
   
    def subst_packs(self, p1, p2):
        return frozenset(self.pkg_unv_name(x) for x in p1) - frozenset(self.pkg_unv_name(x) for x in p2)

    def get_dir(self, *args):
        return os.path.join(self.path, *args)

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
                if f[0] == '/':
                    ff = y.debug
                else:
                    ff = y.warning

                ff('skip source', f)
    
        if not cnt:
            raise Exception('all sources dead')

    @y.cached_method
    def collect_indices(self):
        return list(self.collect_indices_0())

    def resolve_groups_0(self, pkgs):
        for g in pkgs:
            if g[0] == '@':
                yield from self.resolve_groups_0(y.find(g[1:] + '_group')())
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

    def db_pkg_list(self):
        with self.open_db() as db:
            return self.resolve_groups(db.inst())

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
        with y.open_simple_db(os.path.join(self.path, 'etc', 'upm', 'sys.db')) as db:
            yield InstPropertyDB(db)

    def install(self, pkgs):
        y.info('install {bb}' + ', '.join(pkgs) + '{}')

        def do(inst):
            return y.uniq_list_x(inst + pkgs)

        self.modify(do)

        return self.all_packs_dict() 

    def delete_x(self, pkgs):
        y.info('uninstall {br}' + ', '.join(pkgs) + '{}')

        pkgs = frozenset(pkgs)

        def do(inst):
            for i in inst:
                if i not in pkgs:
                    yield i

        self.modify(do)

    def modify(self, func):
        with self.open_db() as db:
            try:
                next_state = list(func(db.inst()))
                db.set_inst(next_state)
                self.apply_db(db)
            except Exception as e:
                try:
                    db.restore_state()
                    self.apply_db(db)
                finally:
                    raise e

    def apply_db(self, db):
        self.actual_install(db.inst())

    def install_one_pkg(self, p, join, pb):
        ppath = self.pkg_dir() + '/' + p['path']
        ppath_tmp = y.tmp_name(self.pkg_dir() + '/' + p['path'])
        pkg_data, data = join()

        def func():
            y.write_file(os.path.join(self.path, 'pkg', 'cache', p['path']), pkg_data)

        with y.defer_context() as defer:
            t = y.threading.Thread(target=func)
            defer(t.join)
            t.start()

            os.makedirs(ppath_tmp)
            self.untar_from_memory(data, ppath_tmp)
            os.rename(ppath_tmp, ppath)

            outs = []

            shell = os.path.join(ppath, '../../bin/sh')

            if not os.path.exists(shell):
                shell = '/bin/sh'

            try:
                out = sp.check_output([shell, '-c', '. ../profile; ' + shell + ' ./install ' + p['path']], cwd=ppath, shell=False)
                out = out.decode('utf-8')
                out = out.strip()

                if out:
                    outs.append(out)
            except Exception as e:
                outs.append(str(e))

            if outs:
                y.info('from install script :\n' + '\n'.join(outs))

            y.info(pb.next_str() + ' {bb}' + ppath + '{}')

    def thr_fetch(self, p):
        res = []

        def fetch_func():
            try:
                res.append(self.fetch_package(p))
                res.append(y.decode_prof(res[0]))
            except Exception as e:
                res.clear()
                res.append(e)

        t = y.threading.Thread(target=fetch_func)
        t.start()

        def join():
            t.join()

            if len(res) == 1:
                raise res[0]

            return res[0], res[1]

        return join

    def actual_install(self, pkgs):
        lst = self.pkg_list(pkgs)

        def to_install():
            for p in lst:
                path = self.pkg_dir() + '/' + p['path']

                if os.path.isdir(path):
                    y.debug('skip', path)
                else:
                    yield p

        to_inst = list(to_install())
        to_wait = [(p, self.thr_fetch(p)) for p in to_inst]

        pb = ProgressBar(len(to_inst))

        for p, j in to_wait:
            self.install_one_pkg(p, j, pb)

        def iter_path():
            for x in reversed(lst):
                yield '/pkg/' + x['path'] + '/bin'
                yield '/pkg/' + x['path'] + '/sbin'

                if len(self.path) > 1:
                    yield self.path + '/pkg/' + x['path'] + '/bin'
                    yield self.path + '/pkg/' + x['path'] + '/sbin'

        def iter_profile():
            yield 'export PATH=' + ':'.join(iter_path())

        profile = '\n'.join(iter_profile()) + '\n'

        y.write_file(self.pkg_dir() + '/profile', profile, mode='w')

        in_use = frozenset([x['path'] for x in lst] + ['cache', 'profile'])
        on_disk = list(os.listdir(self.pkg_dir()))
        pb = ProgressBar(len(frozenset(on_disk) - in_use))

        for x in on_disk:
            if x not in in_use:
                p = os.path.join(self.pkg_dir(), x)

                y.warning(pb.next_str() + ' {br}' + p + '{}')

                try:
                    y.shutil.rmtree(p)
                except OSError:
                    os.unlink(p)

    def fetch_package(self, pkg):
        return pkg['index'].fetch(pkg['path'])

    def init_place(self):
        try:
            os.makedirs(self.path)
        except OSError:
            pass

        with self.open_db() as db:
            db.set_target(self.info)
            db.add_index_file(['http://index.uberpackagemanager.xyz', y.upm_root() + '/r', '/pkg/cache'])

        base = self.pkg_list(['base'])[0]

        self.untar_from_memory(y.decode_prof(self.fetch_package(base)), self.path)

        for f in ('build', 'install'):
            os.unlink(os.path.join(self.path, f))

        y.shutil.rmtree(os.path.join(self.path, 'log'))

        packs = self.install(['tar-run', 'busybox', 'dash-run'])
        safe_symlink('../pkg/' + packs['dash-run'] + '/bin/dash', self.path + '/bin/sh')

        packs = self.install(['upm-run'])
        safe_symlink('../pkg/' + packs['upm-run'] + '/bin/upm', self.path + '/bin/upm')
        self.delete_x(['busybox'])

    def add_indexes(self, indexes):
        with self.open_db() as db:
            db.add_index_file(indexes)
