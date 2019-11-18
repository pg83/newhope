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


@y.main_entry_point
def cli_selftest(args, verbose):
   for f in iter_all_tests():
      y.xprint_white('-------------------------------------------------------------------')

      try:
         f()
      except Exception as e:
         y.xxprint(e, init='{r}')
         
      y.xprint_white('-------------------------------------------------------------------')


def self_test3():
   @y.run_by_timer(0.3)
   def f1():
      print 'f1'


   @y.run_by_timer(1.0)
   def f2():
      print 'f2'

   y.time.sleep(5)
