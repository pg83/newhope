class PropertyDB(object):
    def __init__(self, db):
        self.db = db
        self.ensure('images', {})
        self.ensure('kv', {})

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
