import imp


class StringImporter(object):
   def __init__(self, modules):
       self._modules = dict(modules)
       self._compiled = {}

   def find_module(self, fullname, path):
      if fullname in self._modules.keys():
         return self
      return None

   def load_module(self, fullname):
      if not fullname in self._modules.keys():
         raise ImportError(fullname)

      if fullname in self._compiled:
         return self._compiled[fullname]

      new_module = imp.new_module(fullname)
      exec self._modules[fullname] in new_module.__dict__
      self._compiled[fullname] = new_module

      return new_module


def install():
   import sys

   sys.meta_path.append(StringImporter(modules))
######
import os
import sys
import json
import base64


def prepare_data():
   path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   res = {}

   def iter_lines():
      for m in os.listdir(path + '/upm'):
         if '~' in m:
            continue

         if '#' in m:
            continue

         if '__init__' in m:
            continue

         if m.endswith('.py'):
            with open(path + '/upm/' + m, 'r') as f:
               data = f.read()
               delim = '######'
               p = data.find(delim)

               if p > 0:
                  data = data[0:p]

               mm = 'upm_' + m[:-3]
               epilogue = '__file__ = "' + mm + '.py"\n__name__ = "' + mm + '"\n\n'

               res[mm] = epilogue + data.replace('from .', 'from upm_')

      yield '#!/usr/bin/env python'
      yield '\n'
      yield 'import json'
      yield 'import base64'
      yield '\n'
      yield 'modules = json.loads(base64.b64decode("' + base64.b64encode(json.dumps(res))+ '"))'
      yield '\n'
      yield res['upm_release_me']
      yield '\n'

      with open(path + '/cli', 'r') as f:
         yield '__file__ = "__main__"'
         yield '__name__ = "__main__"'

         yield f.read().replace('# replace me', 'install()')

   return '\n'.join(iter_lines())
