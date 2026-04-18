# Решение
for x in '0123456':
    for y in '0123456':
        p1=f'{y}{x}320'
        p2=f'1{x}3{y}3'
        r=int(p1,7)+int(p2,9)
        if r%181==0:
            print(r//181)




answer = 148

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(14, 1402, answer, '47d1e990583c9c67424d369f3414728e'))