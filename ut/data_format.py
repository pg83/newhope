import lzma
import zstd
import marshal


def decode_prof(data):
    return marshal.loads(zstd.decompress(data))


def encode_prof(v):
    return zstd.compress(marshal.dumps(v), 5)


class SimpleDB(object):
    def __init__(self, path):
        self.path = y.os.path.expanduser(path)

        try:
            y.os.makedirs(y.os.path.dirname(self.path))
        except OSError:
            pass

    def read_db(self):
        try:
            y.debug('{bb}open db ' + self.path + '{}')

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


def get_key(db, k, default):
    if k not in db:
        db[k] = default

    return db[k]


@y.contextlib.contextmanager
def open_simple_db(path):
    db = SimpleDB(path)
    data = db.read_db()
    md5 = y.burn(y.json.dumps(data, sort_keys=True))

    try:
        yield data
    finally:
        new_md5 = y.burn(y.json.dumps(data, sort_keys=True))

        if md5 == new_md5:
            y.debug('db not changed, not write it')
        else:
            db.write_db(data)
