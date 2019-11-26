@y.main_entry_point
def cli_eval(args):
   run_eval(args)


def run_eval(args):
   repl = {
      'layers': 'y.gen_all_texts(only_print_layers=True)'
   }

   if not args:
      for k, v in repl.items():
         y.xprint_b(k, '=', v)

      return

   y.pubsub.run(init=[mf_function_holder])

   for a in args:
      try:
         print(eval(repl.get(a, a)))
      except:
         y.print_tbx(tb_line='can not run ' + a)
