class PkgMngr(object):
    def __init__(self, info, path='/'):
        if not info:
            try:
                with open(path + '/etc/upm/target', 'r') as f:
                    info = f.read().strip()
            except OSError:
                pass

        if not info:
            info = y.small_repr(
                {
                    'os': y.platform.system().lower(),
                    'arch': y.platform.machine()
                }
            )
    
        self.path = path
        self.info = info

    def get_dir(self, *args):
        return y.os.path.join(self.path, *args)

    def get_dir_simple(self, args):
        return (self.path + args).replace('//', '/')
        
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
                if p + '-' in i['path']:
                    by_time.append(i)

        return sorted(by_time, key=lambda x: x['ts'])

    def pkg_list(self, pkgs):
        dd = {}
        
        for l in self.search_pkgs(pkgs):
            p1, p2 = l['path'].split('-v5')
            dd[p1] = l
            
        if len(dd) != pkgs:
            raise Exception('not all packages found')

        return dd.values()
    
    @y.contextlib.contextmanager
    def open_db():
        with y.open_simple_db(y.os.path.join(self.path, 'etc', 'db', 'sys.db')) as db:
            yield PropertyDB(db)
    
    def install(self, pkg):
        lst = self.pkg_list(pkgs)
        
        print lst
