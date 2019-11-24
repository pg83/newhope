def run_stage2(args, builtin, data, **kwargs):
   args, verbose, profile = y.parse_args(y.sys.argv)

   def run_thr():
      fd = {
         'file_data': data, 
         'builtin_modules': builtin,
         'verbose': verbose,
         'need_profile': profile,
         'args': args,
      }

      y.Loader(fd['builtin_modules']).create_module('ya.iface').run_stage4_0(fd)

   t = y.threading.Thread(target=run_thr)
   t.start()
