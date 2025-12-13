# Решение
print('x y z w')
for x in range(2):
    for y in range(2):
        for z in range(2):
            for w in range(2):
                if ((x==y)<=(not(z) or w)) == (not((w<=x) or (y<=z))):
                    print(x, y, z, w)







answer ="wzyx"

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(2, 2, answer, 'e0abee87e4ba1de22c6b8cf076c5016b'))