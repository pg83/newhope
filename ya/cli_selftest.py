def self_test1():
   @y.cached(seed=1)
   def f1(a, b):
      return a + b

   @y.cached(seed=187564)
   def f2(a, b):
      return a + b

   def f3(a, b):
      return a + b

   for i in range(0, 5):
      y.xprint_blue(f1(i, i * 13 - 17), f2(i, i * 13 - 17), f3(i, i * 13 - 17))


def self_test2():
   for color in y.color_map_func():
      y.xxprint('{color}color{}'.format(color=color))

   
def iter_all_tests():
    yield self_test1
    yield self_test2
    yield self_test3


@y.verbose_entry_point
def cli_test_self(args, verbose):
   print 1
   
   with y.abort_on_error():
      for f in iter_all_tests():
         f()
