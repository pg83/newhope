import json
import hashlib


def gen_id(s):
    return hashlib.md5(json.dumps([s, 1], sort_keys=True, indent=4)).hexdigest()
