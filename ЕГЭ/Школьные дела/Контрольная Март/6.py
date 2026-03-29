import sys

sys.setrecursionlimit(10**6)

def g(n):
    if n <= 9:
        return 3 * n
    else:
        return g(n - 4) + 2
def f(n):
    return g(n - 1) + g(n - 3)

print(f(42999))
