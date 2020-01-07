# fibonacci.py
Performant? implementation of the fibonacci function on Python.

The function `fibonacci(n)` returns the nth term of the fibonacci sequence.

Mainly uses memoization and some cache "manipulation", running on a single thread.

## Timing data
Closely follows O(N^2), getting to around 230 seconds for the millionth term in the fibonacci sequence.

[google sheets](https://docs.google.com/spreadsheets/d/1oc8C6XiMK76UYEfWCJn99ASkJvnF8wiNLXIwTk0jwvY/edit?usp=sharing)

## Space
Two modes of operation: 
 - The first saves every possible result in the memoization cache, making successive calls extremely performant, but taking up space relative to N. The simple dict cache crashes on around N > 200000 due to MemoryError.
 - The second keeps a cache of only the last few calls, making successive calls take the full execution time, yet takes up negligible space

Changing between modes of operation is made commenting the CACHE_MAX check marked inside the `memoized` function
