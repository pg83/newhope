import imp
import sys
import json
import base64
import zlib
import os

from upm_iface import y


def prepare_data():
   repl = 'builtin_modules = json.loads(zlib.decompress(base64.b64decode("' + base64.b64encode(zlib.compress(json.dumps(sys.builtin_modules))) + '")))'

   with open(y.script_path(), 'r') as f:
      data = f.read()
      data = data.replace('## builtin_modules', repl)

   return data
