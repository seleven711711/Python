# Решение
for x in '0123456789abcde':
    p1=f'7418{x}{x}461'
    p2=f'719625{x}4'
    p3=f'396{x}99'
    r=int(p1,22)+int(p2,22)+int(p3,22)
    if r%21==0:
        print(r//21)
        break






answer = ...

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(14, 1405, answer, '04ffec330b9d276c1c81c59c1d1a4376'))