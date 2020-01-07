from collections.abc import Hashable
from functools import partial
from itertools import islice

import cProfile
import time


CACHE_MAX = 300
cache = {}

# from https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
# modified to keep a global cache between calls with a max number of elements
# also a little simplified
class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
   def __call__(self, *args):
      global cache
      # keep a cache only big enough to feed a stack-length of calls
      # e.g. no need in keeping the return value of fib(1) if I'm in the 1000s.
      # Commenting the next two lines makes it take up space relative to N,
      # but makes successive calls performant
      if len(cache) > CACHE_MAX:
          cache = dict(islice(cache.items(), CACHE_MAX - 1, len(cache)))
      if args in cache:
         return cache[args]
      else:
         value = self.func(*args)
         cache[args] = value
         return value
    

@memoized
def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n - 2) + fib(n - 1)


def fibonacci(n):
    i = 1
    aux = n
    while aux > CACHE_MAX:
        # populate cache outside of recursion stack
        # moving in increments of CACHE_MAX to move the cache within range
        fib(CACHE_MAX*i)
        aux = aux - CACHE_MAX
        i = i + 1
    return fib(n)


if __name__ == '__main__':
    num = int(input('num: '))
    while not num == 0:
        start = time.time()
        fibonacci(num)
        end = time.time()
        print(f'time: {end - start}')
        print(f'cache length: {len(cache)}')
        num = int(input('num: '))

