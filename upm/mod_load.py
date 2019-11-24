import sys
import random


def ycompile(a, b, c, **kwargs):
   return compile('\n' * kwargs.get('firstlineno', 0) + a, b, c)


class Mod(dict):
   def __init__(self, name, loader):
      self.__dict__ = self
      self.__yid__ = str(int(random.random() * 10000))
      self.__name__ = name
      self.__loader__ = loader
      self.__loader__._by_name[self.__name__] = self
      self.__file__ = self.__name__
      self.__pkg__ = None
      self.__ytext__ = ''
      self.__ylineco__ = 0
      self.__ycode__ = []
      self.__yexec__ = self.exec_data
      self.__last_reindex__ = 0
      self.__ylog__ = lambda: self.y.logging.getLogger(self.__name__)

      try:
         self.y = loader.get_y()
      except:
         pass

      self.exec_text_part(self.builtin_data())

   def self_exec(self):
      self.exec_text_part(self.pop('__ynext_part__', ''))

   def exec_data(self, data, **kwargs):
      return self.__loader__.exec_code(self, data, **kwargs)

   def set_next_part(self, text):
      if text:
         self.__ynext_part__ = text         

   def exec_text_part(self, part):
      if not part.strip():
         return 

      code = ycompile(part, self.__file__.replace('.', '/') + '.py', 'exec', firstlineno=self.line_count())
      
      exec(code, self.__dict__)

      if self.__ytext__:
         self.__ytext__ += '\n'

      self.__ytext__ += part
      self.__ytext__ += '\n'
      self.__ylineco__ = self.__ytext__.count('\n')
      self.__ycode__.append(code)

      self.reindex()

   def reindex(self):
      lc = self.line_count()

      if 2 * self.__last_reindex__ < lc:
         try:
            func = self.y.reindex_module
         except:
            func = None

         if func:
            func(self)

         self.__last_reindex__ = lc

   def line_count(self):
      return self.__ylineco__

   def text(self):
      return self.__ytext__

   def line_count_part(self, text):
      return text.count('\n')

   def builtin_data(self):
      return self.__loader__.builtin_data(self)


class Loader(object):
   def __init__(self, builtin={}):
      self._by_name = {}
      self._builtin = builtin
      self._order = []
      self.create_module('ya')
      self.create_module('gn')
      self.create_module('pl')

   def create_module(self, name):
      if name in self._by_name:
         return self._by_name[name]

      res = Mod(name, self)
      self._order.append(name)

      return res

   def builtin_data(self, mod):
      return self._builtin.get(mod.__name__, {}).get('data', '')

   def exec_code(self, mod, data, module_name=None, **kwargs):
      if module_name:
         m = self.create_module(module_name)

         if data != m.builtin_data():
            m.exec_text_part(data)

         return m

      mod.exec_text_part(data)

      return mod

   def get_y(self):
      return self._by_name['ya.iface'].y

   def get_source(self, name):
      return self._by_name[name].text()
      
   def iter_modules(self):
      return self._by_name.itervalues()

   def save(self):
      return y.zlib.encode(y.marshal.dumps({
         'builtin': self._builtin,
         'modules': [{'name': name, 'text': self._by_name[name].text()} for name in self._order]
      }))

   def load(self, data):
      data = y.marshal.loads(y.zlib.decode(data))
      loader = Loader()

      for x in reversed(data['modules']):
         mod = loader.create_module(x['name'])
         mod.exec_text_part(x['data'])

      loader._builtin = data['builtin']


def bootstrap(mod, args, builtin, **kwargs):
   loader = Loader(builtin)
   mod1 = loader.create_module('ya.iface')
   mod1 = loader.create_module('ya.init_log')
   mod1 = loader.create_module('ya.args_parse')
   mod2 = loader.create_module('ya.mod_load')
   mod2.__loader__.create_module('ya.stage2').run_stage2(args, **args)
