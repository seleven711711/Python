# Решение
for x in '0123456789abc':
    for y in '0123456789abc':
        p1=f'8{x}78{y}'
        p2=f'79{x}{y}7'
        r=int(p1,13)+int(p2,18)
        if r%9==0:
            print(r//9)
            break






answer =114692

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(14, 1401, answer, '436fc6a87245490c1c09148823eec9ff'))