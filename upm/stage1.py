import sys


def create_main(args, data, qq):
   sys.modules['ya'] = -1
   sys.modules['gn'] = -1
   sys.modules['pl'] = -1

   def re_exec(args, qq, **kwargs):
      code = """
def new_main(args, data, qq, **kwargs):
    builtin = dict((x['name'].replace('/', '.')[:-3], x) for x in data)
    mod = Loader(builtin).create_module('ya.mod_load')
    args['builtin'] = builtin
    mod.bootstrap(mod, args, **args)

new_main(args, **args)
"""
      ctx = {'Loader': Loader, 'args': args}
      exec compile(code, '2:stage1.py', 'exec') in ctx
      ctx.clear()

   return re_exec


def run_stage1(args, data, qq, **kwargs):
   re_exec = create_main(args, data, qq)

   ctx = {'re_exec': re_exec, 'args': args}
   exec compile('re_exec(args, **args)', '1:stage1.py', 'exec') in ctx
   ctx.clear()
