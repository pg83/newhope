import sys
import threading
import thread
import signal


def load_builtin_modules(data, builtin):
   initial = (
      'ya.args_parse',
      'ya.algo',
      'ya.single',
      'ya.pub_sub',
      'ya.manager',
      'ya.caches',
      'ya.logwrap',
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
def vault():
    qq = y.homeland_queue

    while True:
        try:
           qq.get()()
        except StopIteration:
           def func():
               raise StopIteration()

           qq.get = func

           return
        except SystemExit as e:
           raise e
        except Exception as e:
           print >>y.sys.stderr, e 
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

   def thr_func_wrapper():
      try:
         try:
            return thr_func()
         except:
            err = sys.exc_info()

            def reraise():
               t.join()
               raise err[0], err[1], err[2]

            qq.put(reraise)
      finally:
         def raise_stop():
            raise StopIteration

         qq.put(raise_stop)
   
   t = threading.Thread(target=thr_func_wrapper)
   t.start()
