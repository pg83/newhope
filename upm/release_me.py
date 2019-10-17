import imp
import sys
import json
import base64
import zlib


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
   builtin_modules = {}
   ## builtin_modules
   sys.meta_path.append(StringImporter(builtin_modules))
######
import os

from .user import load_plugins_code
from .subst import subst_kv_base


def gen_data(name, data):
   return name + ' = json.loads(zlib.decompress(base64.b64decode("' + base64.b64encode(zlib.compress(json.dumps(data)))+ '")))'


def gen_replace(name, data):
   return '## ' + name, gen_data(name, data)


def prepare_data():
   path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   res = {}

   def iter_replaces_upm_user():
      yield gen_replace('builtin_plugins', load_plugins_code(path + '/plugins'))

   def iter_replaces_cli():
      yield ('## release_me', res.pop('upm_release_me'))
      yield gen_replace('builtin_modules', res)
      yield ('## install_me', 'install()')

   def iter_replaces_upm():
      yield ('from .', 'from upm_')

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
            res[mm] = '__file__ = "' + mm + '.py"\n__name__ = "' + mm + '"\n\n' + data

   def iter_main():
      yield '#!/usr/bin/env python'
      yield '## release_me'
      yield '\n'
      yield '__file__ = "__main__"'
      yield '__name__ = "__main__"'

      with open(path + '/cli', 'r') as f:
         yield f.read()

   res['cli'] = '\n'.join(iter_main()) + '\n'

   ll = locals()

   def gen_subst(k):
      def iter_k():
         res = ll.get('iter_replaces_' + k)

         if res:
            yield res

         yield iter_replaces_upm

      return lambda: (k, subst_kv_base(res[k], *[it() for it in iter_k()]))

   def iter_f():
      def iter_k():
         order = ['upm_user', 'cli']

         for k in res.keys():
            if k not in order:
               yield k

         for k in order:
            yield k

      for k in iter_k():
         yield gen_subst(k)

   res.update((f() for f in iter_f()))

   if 0:
      for f in iter_f():
         k, v = f()
         res[k] = v

   return res['cli']
