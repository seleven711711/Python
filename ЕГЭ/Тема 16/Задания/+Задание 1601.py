# Решение
def f(n):
    if n%2==0:
        return f(n//2)+3
    elif n%2!=0 and n%3==0:
        return f(n//3)+2
    else:
        return 0
for n in range(1,100000000):
    if f(n)==67:
        print(n)
        break















answer =18874368

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(16, 1601, answer, 'd43416548c620037459b5607111f8eb5'))