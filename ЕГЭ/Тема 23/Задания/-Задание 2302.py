# Решение
def f(x,y):
    if x>y:
        return 0
    if x==y:
        return 1
    return f(x+1,y)+f(x+2,y)+f(x*2,y)
print(f(4,11)*f(11,15)*f(4,13)*f(13,15))








answer =17000

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(23, 2302, answer, 'f899139df5e1059396431415e770c6dd'))