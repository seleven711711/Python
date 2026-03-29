import math

def is_simple(n):
    if n == 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_divs(n):
    divs = set()
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            divs.add(i)
            divs.add(n // i)
    simple_divs = []
    for d in divs:
        if is_simple(d):
            simple_divs.append(d)
    return sorted(simple_divs)


num = 5_700_000
count = 0
while count < 5:
    divs = get_divs(num)
    if len(divs) > 1:
        m = divs[0] + divs[-1]
        if 70_000 < m == (math.isqrt(m) ** 2):
            print(num, m)
            count += 1
    num += 1