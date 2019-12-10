import lzma
import marshal


def decode_prof(data):
    return marshal.loads(lzma.decompress(data))


def encode_prof(v):
    return lzma.compress(marshal.dumps(v))


class SimpleDB(object):
    def __init__(self, path):
        self.path = y.os.path.expanduser(path)
        
        try:
            y.os.makedirs(y.os.path.dirname(self.path))
        except OSError:
            pass
        
    def read_db(self):
        try:
            y.info('{bb}open db ' + self.path + '{}')
            
            with open(self.path, 'rb') as f:
                return decode_prof(f.read())
        except Exception as e:
            y.info('{br}' + str(e) + ', can not load db, reinitialize...{}')

        return {}

    def write_db(self, data):
        y.info('{bg}write new version of ' + self.path + '{}')
        
        with open(self.path, 'wb') as f:
            f.write(encode_prof(data))
            f.flush()
        
    def rcu(self, func):
        self.write_db(func(self.read_db()))


@y.contextlib.contextmanager
def open_simple_db(path):
    db = SimpleDB(path)
    data = db.read_db()
    md5 = y.burn(data)
    
    try:
        yield data
    finally:
        new_md5 = y.burn(data)

        if md5 == new_md5:
            y.info('db not changed, not write it')
        else:
            db.write_db(data)
