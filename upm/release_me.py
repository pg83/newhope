import imp
import sys
import imp
import json
import base64
import zlib
import os
import sys
import signal
import traceback
import random
import subprocess


def script_path():
   try:
      return script_path_ex()
   except Exception:
      pass

   return sys.modules['__main__'].__path__


def prepare_modules_data():
   def iter_parts():
      yield 'builtin_modules = json.loads(zlib.decompress(base64.b64decode("'
      yield base64.b64encode(zlib.compress(json.dumps(sys.builtin_modules)))
      yield '")));'

   return ''.join(iter_parts())


def load_local_code(where, ext='.py'):
   path = os.path.dirname(script_path()) + '/' + where + '/'

   for m in list(os.listdir(path)):
     if '~' in m:
        continue

     if '#' in m:
        continue

     if '__init__' in m:
        continue

     if not m.endswith(ext):
        continue

     mpath = path + m

     with open(mpath, 'r') as f:
        yield mpath, f.read()

   if ext == '.py':
      with open(script_path(), 'r') as f:
         yield path + 'cmd.py', f.read()


def load_program_modules():
   res = {}

   for path, data in load_local_code('upm'):
      res[path] = ('upm_' + os.path.basename(path)[:-3], data)

   return res


def load_plugin_modules():
   res = {}

   for path, data in load_local_code('plugins'):
      res[os.path.basename(path)] = data

   return res


def load_bash_modules():
   res = {}

   for path, data in load_local_code('scripts', ext=''):
      res[os.path.basename(path)] = data

   return res


def install():
   def bm():
      return sys.builtin_modules

   builtin_modules = {}
   ## builtin_modules

   if builtin_modules:
      pass
   else:
      builtin_modules = {
         'upm': load_program_modules(),
         'plu': load_plugin_modules(),
         'mod': load_bash_modules(),
      }

   u = builtin_modules['upm']
   v = builtin_modules['plu']

   keys = {
      'splitter.py': -10000000000000000,
   }

   plugins = sorted(list(v.items()), key=lambda x: keys.get(x[0], -len(x[1])))
   plugins_code = '\n'.join([x[1] for x in plugins])
   sys.builtin_modules = builtin_modules
   mods = []

   for path in bm()['upm'].keys():
      name, value = bm()['upm'][path]

      if name == 'upm_plugins':
         value += plugins_code

      if name not in sys.modules:
         mod = sys.modules.setdefault(name, imp.new_module(name))
         mod.__file__ = path
         mod.__name__ = name
         mod.__pkg__ = name.rstrip('.')[-1]
         mod.__text__ = value
         mods.append((mod, path, value, []))

   prev_order = dict(enumerate(bm().get('ord', [])))
   prev_order['upm_iface'] = -100

   def get_order(x):
      return prev_order.get(x[0].__name__, 0)

   mods = list(sorted(mods, key=get_order))
   order = []

   while mods:
      new_mods = []

      for mod, path, data, exc in mods:
         try:
            try:
               exec compile(data, path, 'exec') in mod.__dict__
               order.append(mod.__name__)
            except Exception as e:
               #print e, path, traceback.print_exc(e)
               new_mods.append((mod, path, data, exc + [e]))

               raise e
         except AttributeError:
            pass
         except ImportError:
            pass

      random.shuffle(new_mods)
      mods = new_mods

   bm()['ord'] = order
   bm()['txt'] = prepare_release_data1()


def prepare_release_data1():
   script_data = sys.modules['upm_cmd'].__text__.replace("__main__':", "__newmain__':")
   script_data = script_data + '\n\n__file__ = "' + script_path() + '"\n'
   script_data = script_data + '\n\n' + sys.modules['upm_release_me'].__text__

   return script_data


def prepare_release_data():
   script_data = sys.builtin_modules['txt']
   script_data = script_data.replace('## builtin' + '_modules', prepare_modules_data())

   return script_data


def run_code_in_new_context(data, mode):
   mod = imp.new_module('__main__')

   mod.__name__ = '"__main__"'
   mod.__file__ = __file__

   def flt():
      for k, v in sys.modules.items():
         if k in ('__builtin__',):
            yield k, v
         else:
            del v

   sys.modules = dict(flt())
   sys.modules['__main__'] = mod
   comp = compile(data + '\n\nbootstrap(%s)\n' % mode, mod.__file__, 'exec')

   exec comp in mod.__dict__


def run_from_now():
   return run_code_in_new_context(prepare_data(), 0)


def run_with_new_python():
   data = prepare_release_data() + '\n\nbootstrap(0)\n'
   p = subprocess.Popen(['/usr/bin/python', '-'] + sys.argv[1:], stdout=sys.stdout, stderr=sys.stderr, stdin=subprocess.PIPE)
   p.communicate(data)
   sys.exit(p.wait())


def bootstrap(mode=0):
   install()

   if mode == 0:
      from upm_iface import y
      sys.exit(y.run_main())
   elif mode == 2:
      run_with_new_python()
   else:
      run_from_now()
      sys.exit(0)
