import sys
import threading


def load_builtin_modules(data, builtin):
   initial = (
      'ya.int_counter',
      'ya.args_parse',
      'ya.algo',
      'ya.err_handle',      
      'ya.single',
      'ya.caches',
      'ya.defer',
      'ya.pub_sub',
      'ya.manager',
      'ya.mini_db',
      'ya.noid_calcer',
      'ya.gui',
      'ya.gui_ext',
   )

   for m in initial:
      mod = __loader__.create_module(m)

   initial = set(initial)

   for k in builtin:
      if k not in initial:
         if k.startswith('ya'):
            __loader__.create_module(k)
            initial.add(k)


def run_stage2(args, builtin, data, qq, **kwargs):
   def thr_func():
      args, verbose, profile = y.parse_args(sys.argv)
      
      fd = {
         'file_data': data, 
         'builtin_modules': builtin, 
         'homeland_queue': qq,
         'verbose': verbose,
         'need_profile': profile,
      }
      
      @y.lookup
      def lookup(name):
         return fd[name]
      
      load_builtin_modules(data, builtin)
      
      fd['signal_channel'] = y.get_signal_channel()
      fd['main_channel'] = y.get_main_channel()
      
      y.init_vault()
      y.run_defer_constructors()
      y.run_main(args)

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
