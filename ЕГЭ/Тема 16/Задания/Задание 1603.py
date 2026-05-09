# Решение
def f(n):
    if n==0:
        return 0
    return f(n//10)+(n%10)
c=0









answer = ...

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(16, 1603, answer, '383d228fc45e55c06236b5d6278e1765'))