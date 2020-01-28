import sys
import random

/*
def cons_to_name_xx(c):
    if not c:
        return 'nop'

    try:
        c = c['target']
    except KeyError:
        pass

    res = ''

    for k, f in (('os', 1), ('libc', 1), ('arch', 2)):
        if k in c:
            res += c[k][:f]

    return res


def small_repr_x(c):
    return cons_to_name_xx(c)
*/
 
class Mod(dict):
   def __init__(self, name, loader):
      self.__dict__ = self
      self.__yid__ = str(int(random.random() * 1000000000))
      self.__name__ = name
      self.__loader__ = loader
      self.__file__ = self.__name__
      self.__pkg__ = None
      self.__ytext__ = ''
      self.__ylineco__ = 0
      self.__ycode__ = []
      self.__yexec__ = self.exec_data
      self.__last_reindex__ = 0
      self.__sub__ = {}
  
      def get_log():
         log = self.y.logging.getLogger(self.__name__)

         self.__ylog__ = lambda: log

         return self.__ylog__()
 
      self.__ylog__ = get_log
  
      try:
         self.y = loader.get_y()
      except Exception:
         pass

      self.__loader__.register_module(self)
      self.exec_text_part(self.builtin_data())

   def ycompile(self, a, b, c, **kwargs):
      ap = self.__loader__._preproc(a, args=kwargs.get('args', {}))

      return self.__loader__._g.compile('\n' * kwargs.get('firstlineno', 0) + ap, b, c)
   
   def vname(self):
      return self.__name__[len(self.__loader__.root_module().__name__) + 1:]
  
   def create_sub_module(self, name):
      if (pos := name.find('.')) > 0:
         return self.create_sub_module_0(name[:pos]).create_sub_module(name[pos + 1:])

      return self.create_sub_module_0(name)

   def create_sub_module_0(self, name):
      if name not in self.__sub__:
         self.__sub__[name] = Mod(self.full_name(name), self.__loader__)

      return self.__sub__[name]
  
   def self_exec(self):
      self.exec_text_part(self.pop('__ynext_part__', ''))

   def exec_data(self, data, **kwargs):
      return self.__loader__.exec_code(self, data, **kwargs)

   def set_next_part(self, text):
      if text:
         self.__ynext_part__ = text 

   def exec_text_part(self, part, args={}):
      if not part.strip():
         return

      code = self.ycompile(part, self.__file__.replace('.', '/') + '.py', 'exec', firstlineno=self.line_count(), args=args)
  
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
         except Exception:
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

   def full_name(self, sub):
      return self.__name__ + '.' + sub
   

class Loader(object):
   def __init__(self, name, g):
      self.__name__ = name
      self._by_name = {}
      self._builtin = g.builtin_modules
      self._order = []
      self._g = g
      self._preproc = lambda text, **kwargs: text
  
      Mod(name, self)
  
   def root_module(self):
      return self._by_name[self._order[0]]
  
   def create_module(self, name):
      fname = self.root_module().full_name(name)
  
      if fname in self._by_name:
         return self._by_name[fname]

      return self.root_module().create_sub_module(name)

   def register_module(self, mod):
      mn = mod.__name__

      assert mn not in self._by_name
  
      self._order.append(mn)
      self._by_name[mn] = mod
  
      return mod
   
   def builtin_data(self, mod):
      return self._builtin.get(mod.vname(), {}).get('data', '')

   def exec_code(self, mod, data, module_name=None, arch={}, **kwargs):
      args = arch.copy()
  
      if args:
         module_name = self.get_y().small_repr(args) + '.' + module_name
 
         args.update({
            '__OS__' : '"' + arch['os'].upper() + '"',
            '__ARCH__': '"' + arch['arch'].upper() + '"',
            '__' + arch['arch'].upper() + '__': '1',
            '__' + arch['os'].upper() + '__':  '1',
         })
 
      if module_name:
         m = self.create_module(module_name)

         if data != m.builtin_data():
            m.exec_text_part(data, args=args)

         return m

      mod.exec_text_part(data)

      return mod

   def find_sub_module(self, name):
      return self._by_name[self.root_module().full_name(name)]
   
   def get_y(self):
      return self.find_sub_module('ut.iface').y

   def get_source(self, name):
      return self._by_name[name].text()
  
   def iter_modules(self):
      for k in self._order:
         yield self._by_name[k]


def bootstrap(g):
    loader = Loader('1', g)

    loader.create_module('ut.iface')
    loader.create_module('ut.args_parse')
    loader.create_module('ut.mod_load')
    __loader__.__dict__.clear()
    loader.create_module('ut.stage2').run_stage2(g)
