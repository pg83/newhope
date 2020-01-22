def compactify(l):
    return list(reversed(list(y.uniq_list_0(reversed(l)))))


class PropertyDB(object):
    def __init__(self, db):
        self.db = db
        self.ensure('images', {})
        self.ensure('kv', {})

        for k in list(self.db.keys()):
            if k not in ('kv', 'images'):
                self.db.pop(k)

        for k in list(self.images.keys()):
            self.images[k] = compactify(self.images[k])
                
    def ensure(self, k, d):
        y.get_key(self.db, k, d)

    @property
    def images(self):
        return self.db['images']
    
    @property
    def kv(self):
        return self.db['kv']


@y.contextlib.contextmanager
def open_pdb():
    with y.open_simple_db('~/.upmdb') as db:
        yield PropertyDB(db)
