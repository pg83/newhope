import hashlib
import marshal
import json

from hashlib import md5
from marshal import dumps


def burn(p):
    return md5(dumps(p)).hexdigest()[:16]


def struct_dump_bytes_json(p):
    return md5(json.dumps(p, sort_keys=True)).hexdigest()
