# Решение при помощи Рекурсии
"""
def f(n):
    if n % 2 == 0:
        return f(n // 2) + 3
    elif n % 2 == 1 and n % 3 == 0:
        return f(n // 3) + 2
    else:
        return 0

n = 1
while f(n) != 70:
    n += 1
print(n)
"""

# Решение при помощи Списка
res = [0] * 100000000
for n in range(1, 100000000):
    if n % 2 == 0:
        res[n] = res[n // 2] + 3
    elif n % 2 == 1 and n % 3 == 0:
        res[n] = res[n // 3] + 2
    else:
        res[n] = 0
for n in range(1, 100000000):
    if res[n] == 70:
        print(n)
        break

