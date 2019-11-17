import sys
import threading
import thread
import signal


def load_builtin_modules(data, builtin):
   initial = (
      'ya.int_counter',
      'ya.args_parse',
      'ya.algo',
      'ya.single',
      'ya.defer',
      'ya.caches',
      'ya.pub_sub',
      'ya.manager',
      'ya.mini_db',
      'ya.noid_calcer',
   )

   for m in initial:
      mod = __loader__.create_module(m)

   initial = set(initial)

   for k in builtin:
      if k not in initial:
         if k.startswith('ya'):
            __loader__.create_module(k)
            initial.add(k)


def send_module_back():
   mod = __loader__.create_module('ya.__main__')
   mod.y = y
   mod.exec_text_part(""" 
def vault1():
    qq = y.homeland_queue
    pp = y.print_tbx

    while True:
        try:
           qq.get()()
        except SystemExit as e:
           raise e
        except:
           try:
               pp()
           except:
               pass

           raise SystemExit(1)

def vault():
    channel = y.write_channel('die soon', 'vault')

    try:
        return vault1()
    finally:
        channel({'die': 'soon'})
   """)

   y.homeland_queue.put(mod.vault)


def set_sigint():
   def sig(*args):
      sig.__c({'value': 'SIGINT', 'args': args})

   sig.__c = y.write_channel('SIGINT', 'sh')
   signal.signal(signal.SIGINT, sig)


def run_stage2(args, builtin, data, qq, **kwargs):
   def thr_func():
      fd = {
         'file_data': data, 
         'builtin_modules': builtin, 
         'homeland_queue': qq,
      }

      @y.lookup
      def lookup(name):
         return fd[name]

      load_builtin_modules(data, builtin)
      send_module_back()
      qq.put(set_sigint)
      y.run_main(sys.argv)
      y.prompt('/theend')

   def thr_func_wrapper():
      try:
         thr_func()

         raise SystemExit(0)
      except:
         err = sys.exc_info()

         def reraise():
            t.join()

            raise err[0], err[1], err[2]

         qq.put(reraise)
   
   t = threading.Thread(target=thr_func_wrapper)
   t.start()
