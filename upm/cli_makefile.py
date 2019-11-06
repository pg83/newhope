@y.main_entry_point
def cli_makefile(arg, verbose):
   parser = y.argparse.ArgumentParser()

   parser.add_argument('-o', '--output', default='', action='store', help='file to output, stdout by default')
   parser.add_argument('-S', '--shell', default=[], action='append', help='out build.sh script')
   parser.add_argument('-P', '--plugins', default=[], action='append', help='where to find build rules')
   parser.add_argument('-I', '--internal', default=False, action='store_const', const=True, help='generte internal format')

   args = parser.parse_args(arg)

   if args.output:
      f = open(args.output, 'w')
      close = f.close
   else:
      f = y.sys.stdout
      close = lambda: 0

   try:
      if args.shell:
         f.write(y.build_sh_script(args.shell, verbose))
      else:
         f.write(y.main_makefile(verbose, internal=args.internal))

      f.flush()
   finally:
      close()
