@y.main_entry_point
def cli_makefile(arg):
   parser = y.argparse.ArgumentParser()
   
   parser.add_argument('-o', '--output', default='', action='store', help='file to output, stdout by default')
   parser.add_argument('-S', '--shell', default=[], action='append', help='out build.sh script')
   parser.add_argument('-P', '--plugins', default=[], action='append', help='where to find build rules')
   parser.add_argument('-I', '--internal', default=False, action='store_const', const=True, help='generte internal format')
   parser.add_argument('-D', '--built-set', default=[], action='append', help='build set for build, like distro')
   parser.add_argument('-T', '--dot', default=False, action='store_const', const=True, help='output dot graph')

   args = parser.parse_args(arg)

   if args.built_set:
      for bs in args.built_set:
         y.solve_build(bs)

      return

   with y.defer_context() as defer:
      if args.output:
         f = open(args.output, 'w')
         defer(f.close)
      else:
         f = y.stdout

      def main_func():
         if args.dot:
            f.write(y.build_dot_script())
         elif args.shell:
            f.write(y.build_sh_script(args.shell))
         else:
            f.write(y.main_makefile(internal=args.internal))

         f.flush()

      main_func()
