from collections.abc import Hashable
from functools import partial
from itertools import islice

import cProfile
import time
import pstats
from pstats import SortKey


# MemoryError at ~210000
CACHE_MAX = 5
STACK_MAX = 600
cache = {}

# from https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
# modified to keep a global cache between calls with a max number of elements
# and to work with just one parameter for simplicity
def memoized(func):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def funcall(num):
        global cache
        if num in cache:
            # print(f'found {num} in cache')
            return cache[num]
        else:
            value = func(num)
            cache[num] = value
            '''
            keep a cache only big enough to feed a stack-length of calls
            e.g. no need in keeping the return value of fib(1) if I'm in the 1000s.
            '''
            if len(cache) > CACHE_MAX:
                cache = dict(islice(cache.items(), CACHE_MAX - 1, len(cache)))
            return value
    return funcall
    

@memoized
def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n - 2) + fib(n - 1)


def fibonacci(n):
    leading_up = set(range(max(0, n - STACK_MAX + 1), n + 1))
    cache_keys = set(cache.keys())
    if len(cache_keys) == 0:
        cache_keys.add(0)
    if n > max(cache_keys):
        aux = max(cache_keys) + STACK_MAX - 1
    else:
        aux = STACK_MAX - 1
    # print(leading_up)
    print(cache_keys)
    print(f'cache intersection length: {len(leading_up.intersection(cache_keys))}')
    #if not n in set(cache.keys()):
    if len(leading_up.intersection(cache_keys)) == 0:
        while aux < n:
            '''
            populate cache outside of recursion stack
            moving in increments of STACK_MAX to move the cache within range
            starting with the highest number in the cache if n is bigger
            or starting by 0 if it's smaller than anything in there
            '''
            #print(f'populating for {aux}')
            fib(aux)
            aux = aux + STACK_MAX
    return fib(n)


def use_user_input():
    num = int(input('num: '))
    while not num == 0:
        start = time.time()
        value = fibonacci(num)
        end = time.time()
        print(f'time: {end - start}')
        # print(f'results in cache: {list(cache.keys())}')
        print(f'cache length: {len(cache)}')
        # print(f'result: {value}')
        num = int(input('\nnum: '))


def iterate_until_input():
    num = int(input('num: '))
    print(f'getting number in one go')
    start = time.time()
    value = fibonacci(num)
    end = time.time()
    time_one = end - start
    total_time = 0
    print(f'getting {num} terms')
    i = 0
    while i <= num:
        start = time.time()
        value = fibonacci(i)
        end = time.time()
        total_time = total_time + end - start
        #print(f'{i}th term time: {end - start}')
        i = i + 1
    print(f'Time to get the {num}th term in one go: {time_one}')
    print(f'Total time for {num} terms: {total_time}')


def profiler_test():
    cProfile.run('fibonacci(100000)', 'pystats')
    p = pstats.Stats('pystats').strip_dirs()
    p.sort_stats(SortKey.CUMULATIVE).print_stats(10)
    cProfile.run('fibonacci(200000)', 'pystats')
    p = pstats.Stats('pystats').strip_dirs()
    p.sort_stats(SortKey.CUMULATIVE).print_stats(10)
    cProfile.run('fibonacci(300000)', 'pystats')
    p = pstats.Stats('pystats').strip_dirs()
    p.sort_stats(SortKey.CUMULATIVE).print_stats(10)


if __name__ == '__main__':
    use_user_input()
    #profiler_test()
    #iterate_until_input()
