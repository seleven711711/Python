# Решение
def f(n):
    if n==0:
        return 0
    if n%2!=0:
        return f(n-1)+1
    if n>0 and n%2==0:
        return f(n//2)
c = 0
for n in range (0,1000):
    print(n,bin(n),f(n))
    if f(n)==2:
        c+=1
print(c)










answer = 657720

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(16, 1602, answer, 'ddb30680a691d157187ee1cf9e896d03'))