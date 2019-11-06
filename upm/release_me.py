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
import itertools


def rm_script_path():
   try:
      return script_path_ex()
   except Exception:
      pass

   return sys.modules['__main__'].__path__


def rm_prepare_modules_data():
   def iter_parts():
      yield 'builtin_modules = json.loads(zlib.decompress(base64.b64decode("'
      yield base64.b64encode(zlib.compress(json.dumps(sys.builtin_modules)))
      yield '")));'

   return ''.join(iter_parts())


def rm_load_local_code(where):
   path = os.path.dirname(rm_script_path()) + '/' + where + '/'

   for m in list(os.listdir(path)):
     if '~' in m:
        continue

     if '#' in m:
        continue

     if '__init__' in m:
        continue

     if m == 'release_me.py':
        continue

     mpath = path + m

     with open(mpath, 'r') as f:
        yield mpath, f.read()


def rm_load_program_modules():
   res = {}

   for path, data in rm_load_local_code('upm'):
      res[path] = ('ya.' + os.path.basename(path)[:-3], data)

   return res


def rm_fix_plugin_data1(data):
   p1 = data.find('/*')
   p2 = data.find('*/')

   if p1 > 0 and p2 > 0:
      d1 = data[:p1]
      d2 = data[p2 + 2:]

      return d1 + ' ' * (p2 + 2 - p1) + d2

   return data


def rm_load_plugin_modules():
   res = {}

   for path, data in rm_load_local_code('plugins'):
      res[os.path.basename(path)] = rm_fix_plugin_data1(data)

   return res


def rm_load_bash_modules():
   res = {}

   for path, data in rm_load_local_code('scripts'):
      res[os.path.basename(path)] = data

   return res


def rm_create_random_order(lst):
   return dict((x, random.random()) for x in lst)


def rm_create_stable_order(lst):
   return dict((x, i) for i, x in enumerate(lst))


class Mod(dict):
   def __init__(self, name):
      self.__dict__ = self
      self.__name__ = name

      #sys.modules[name] = self

   def self_exec(self):
      exec self.__ycode__ in self


class Loader(object):
   def __init__(self):
      self._by_name = {}
      self.create_module('ya', 'ya', '', 'ya')

   def create_module(self, name, path, text, file=None):
      l = len(os.path.dirname(os.path.dirname(path)))

      m = Mod(name)
      m.__file__ = file or m.__name__
      m.__ypath__ = path
      m.__ytext__ = text
      m.__ycode__ = compile(m.__ytext__.replace('\0', ''), m.__file__, 'exec')
      m.__pkg__ = None
      m.__loader__ = self

      def exec_c(data, **kwargs):
         return m.__loader__.exec_code(m, data, **kwargs)

      m.__yexec__ = exec_c

      self._by_name[m.__name__] = m
      self._by_name['ya'][m.__name__[3:]] = m

      return m

   def exec_code(self, mod, data, closure=None, module_name=None, globals=None, **kwargs):
      if module_name:
         mod_name = mod.__name__ + '.' + module_name
         m = self.create_module(mod_name, mod.__ypath__, data, mod_name)

         if globals:
            m.globals = lambda: globals
            m.locals = lambda: globals

         m.y = mod.y

         if closure:
            m.update(closure)

         m.self_exec()

         return m
      else:
         exec compile(data.strip(), mod.__file__, 'exec') in mod

   def get_y(self):
      return self._by_name['ya.iface'].y

   def get_source(self, name):
      m = self._by_name[name]
      
      return m.__ytext__
      
   def iter_modules(self):
      return self._by_name.itervalues()


def rm_install():
   sys.modules['ya'] = -1

   def bm():
      return sys.builtin_modules

   builtin_modules = {}
   ## builtin_modules

   if builtin_modules:
      pass
   else:
      builtin_modules = {
         'upm': rm_load_program_modules(),
         'plu': rm_load_plugin_modules(),
         'mod': rm_load_bash_modules(),
         'ord': {},
      }

   u = builtin_modules['upm']
   v = builtin_modules['plu']

   def get_plugins_code():
      keys = {
         'splitter.py': -10000000000000000,
      }

      plugins = sorted(list(v.items()), key=lambda x: keys.get(x[0], len(x[1])))

      return '\n'.join(x[1] for x in plugins)
   
   loader = Loader()

   sys.builtin_modules = builtin_modules
   mods = []

   for path in sorted(bm()['upm'].keys()):
      name, value = bm()['upm'][path]

      if name == 'ya.plugins':
         value += get_plugins_code()

      assert name not in sys.modules

      mod = loader.create_module(name, path, value)
      mods.append(mod)

   fix_order = {
      'ya.iface': -100,
      'ya.algo': -95,
      'ya.single': -90,
      'ya.manager': -85,
      'ya.caches': -80,
      'ya.logwrap': -75,
      'ya.mini_db': -70,
      'ya.plugins': 1000000,
   }

   def get_order(porder):
      return lambda x: fix_order.get(x.__name__, porder[x.__name__])

   def mod_names(mo):
      return [m.__name__ for m in mo]

   old_order = dict(rm_create_stable_order(mod_names(mods)).items() + bm()['ord'].items())
   mods = list(sorted(mods, key=get_order(old_order)))
   iface = mods[0]
   used = set()
   order = []

   while mods:
      new_mods = []

      for mod in mods:
         if mod.__name__ != iface.__name__:
            mod.y = iface.y

         try:
            try:
               mod.self_exec()
               order.append(mod.__name__)
            except Exception as e:
               key = str(e) + str(path)

               if key not in used:
                  used.add(key)
                  print e, mod.__name__, traceback.format_exc(e)

               new_mods.append(mod)

               raise
         except AttributeError:
            pass
         except ImportError:
            pass

      random_order = rm_create_random_order(mod_names(new_mods))
      mods = list(sorted(new_mods, key=get_order(random_order)))

   bm()['ord'] = dict(((x, i) for i, x in enumerate(order)))
   bm()['txt'] = rm_get_main_text().replace("__main__':", "__newmain__':")
   
   return iface.y


def rm_get_main_text():
   try:
      return sys.modules['__main__'].__text__
   except AttributeError:
      pass

   return sys.builtin_modules['txt']


def rm_prepare_release_data():
   script_data = sys.builtin_modules['txt']
   script_data = script_data.replace('## builtin' + '_modules', rm_prepare_modules_data())

   return script_data


def rm_run_code_in_new_context(data, mode):
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


def rm_run_from_now():
   return rm_run_code_in_new_context(rm_prepare_data(), 0)


def rm_run_with_new_python(args):
   data = rm_prepare_release_data() + '\n\nbootstrap(0)\n'
   p = subprocess.Popen([sys.executable, '-'] + args[1:], stdout=sys.stdout, stderr=sys.stderr, stdin=subprocess.PIPE)
   p.communicate(data)
   sys.exit(p.wait())


def rm_check_arg_2(args, p, with_arg=False):
   res = {p: None}

   def flt():
      it = itertools.chain(args)

      for x in it:
         if x == p:
            res[p] = True

            if with_arg:
               for y in it:
                  res[p] = y

                  for z in it:
                     yield z

                  return

            for y in it:
               yield y

            return

         yield x

   return list(flt()), res[p]


def check_arg(args, params):
   old_len = len(args)

   for p in params:
      args, _ = rm_check_arg_2(args, p)

   return args, len(args) != old_len


def bootstrap_impl(mode):
   args = sys.argv

   if mode == -1:
      args, mode = rm_check_arg_2(args, '--bootstrap-mode', True)

      if mode:
         mode = int(mode)
      else:
         mode = 0

   y = rm_install()

   if mode == 0:
      y.exec_plugin_code(y.gen_all_texts())

      return y.run_main(args)
   elif mode == 2:
      rm_run_with_new_python(args)
   else:
      rm_run_from_now()

   return 0


def bootstrap(mode=0):
   sys.exit(bootstrap_impl(mode))
