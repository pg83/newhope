def main_makefile(verbose, internal=False):
   def iter():
      host = {'os': 'darwin', 'arch': 'x86_64'}
      cc = {'host': host, 'target': host}

      yield cc
      
   data = ''
   prev = set()

   while True:
      portion = set(y.gen_packs(iter))
      
      len_b = len(prev)
      prev = prev | portion
      len_a = len(prev)

      if len_b == len_a and prev:
         return data

      data = y.build_makefile(sorted(prev), verbose, internal=internal)
