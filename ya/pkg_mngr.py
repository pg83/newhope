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
        if not info:
            try:
                if path:
                    tgpath = y.os.path.join(path, 'etc/upm/target')
                else:
                    tgpath = find_file('etc/upm/target')
            
                with open(tgpath, 'r') as f:
                    info = f.read().strip()

                path = y.os.path.abspath(tgpath)[:-15]
            except OSError:
                pass

        if not info:
            raise Exception("you should provide target platform")

        self.path = path
        self.info = info

        print self.path, self.info

    def get_dir(self, *args):
        return y.os.path.join(self.path, *args)

    def etc_dir(self):
        return self.get_dir('etc')

    def upm_dir(self):
        return self.etc_dir() + '/upm'

    def target_file(self):
        return self.upm_dir() + '/target'

    def get_dir_simple(self, args):
        return (self.path + args).replace('//', '/')

    def pkg_cache_dir(self):
        return self.pkg_dir() + '/cache'

    def pkg_dir(self):
        return self.get_dir('pkg')

    def list_dir(self, path):
        where = y.os.path.join(self.path, path)

        if not y.os.path.isdir(where):
            y.warning('not a directory', where)

            return

        for x in y.os.listdir(where):
            yield x, y.os.path.join(x, where)

    def get_index_files_0(self):
        for p in sorted([p for x, p in self.list_dir('/etc/upm')]):
            y.info('will read', p, 'for index links')

            with open(p, 'r') as f:
                for x in f.read().split('\n'):
                    x = x.strip()

                    if x:
                        y.info('got', x)
        
                        yield x

        yield 'http://index.samokhvalov.xyz/index'

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
                if i['path'].startswith(p + '-'):
                    by_time.append(i)

        return sorted(by_time, key=lambda x: x['ts'])

    def pkg_list(self, pkgs):
        dd = {}

        for l in self.search_pkgs(pkgs):
            p1, p2 = l['path'].split('-v5')
            dd[p1] = l
    
        if len(dd) != len(pkgs):
            raise Exception('not all packages found ' + str(dd))

        return list(dd.values())

    @y.contextlib.contextmanager
    def open_db():
        with y.open_simple_db(y.os.path.join(self.path, 'etc', 'db', 'sys.db')) as db:
            yield PropertyDB(db)

    def install(self, pkgs):
        lst = self.pkg_list(pkgs)

        for p in lst:
            data = self.fetch_package(p)
            path = y.os.path.join(self.pkg_cache_dir(), p['path']) + '.tar'

            with open(path, 'wb') as f:
                f.write(y.decode_prof(data))

            ppath_tmp = self.pkg_dir() + '/.' + p['path']
            ppath = self.pkg_dir() + '/' + p['path']
    
            y.os.makedirs(ppath_tmp)
            y.os.system('cd ' + ppath_tmp  + ' && tar -xf ' + path + ' && mv ' + ppath_tmp + ' ' + ppath)
        

    def fetch_package(self, pkg):
        y.info('will fetch package{br}', pkg['path'], '{}')

        return y.fetch_data(y.os.path.dirname(pkg['index']) + '/' + pkg['path'])

    def init_place(self):
        try:
            y.os.makedirs(self.path)
        except OSError:
            pass

        base = self.pkg_list(['base'])[0]

        y.os.chdir(self.path)

        with open(base['path'] + '.tar', 'wb') as f:
            f.write(y.decode_prof(self.fetch_package(base)))
            y.os.system('tar -xf *.tar && rm -rf log base* build')

        with open(self.target_file(), 'w') as f:
            f.write(self.info)
