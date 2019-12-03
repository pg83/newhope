@y.main_entry_point
async def cli_eval(args):
   await run_eval(args)


async def run_eval(args):
   repl = {
      'layers': 'y.gen_all_texts(only_print_layers=True)'
   }

   if not args:
      for k, v in repl.items():
         y.xprint_bb(k, '=', v)

      return

   await y.prepare_makefile()

   for a in args:
      try:
         print(eval(repl.get(a, a)))
      except:
         y.print_tbx(tb_line='can not run ' + a)
