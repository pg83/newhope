import lzma
import marshal


def decode_prof(data):
    return marshal.loads(lzma.decompress(data))


def encode_prof(v):
    return lzma.compress(marshal.dumps(v))
