import hashlib
import marshal
import json


def burn(p):
    return struct_dump_bytes(p)


def struct_dump_bytes(p):
    return hashlib.md5(marshal.dumps(p)).hexdigest()[:16]


def struct_dump_bytes_json(p):
    return hashlib.md5(json.dumps(p, sort_keys=True)).hexdigest()
