``                                                       # Решение
res = [0] * 1000000000
for n in range(1, 1000000000):
    if n==0:
        res[n]=0
    elif n>0 and n%4<2:
        res[n] = res[n // 4] + n % 4
    elif n%4>=2:
        res[n] = res[n //4]+n%4-1
for n in range(1,1000000000):
    if res[n]==27 and res[n+1]==16:
        print(n)
        break







answer = ...

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(16, 1607, answer, '2a0b3b7b30d11559c931dde71e179f16'))