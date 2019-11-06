def main_makefile(verbose, internal=False):
   def iter():
      host = {'os': 'darwin', 'arch': 'x86_64'}
      cc = {'host': host, 'target': host}

      yield cc

   return y.build_makefile(list(y.gen_packs(iter)), verbose, internal=internal)
