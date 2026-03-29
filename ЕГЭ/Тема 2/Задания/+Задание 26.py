# Решение
print('x y z w')
for x in range(2):
    for y in range(2):
        for z in range(2):
            for w in range(2):
                if (w==(not(z==y))) and (z==(y<=x)):
                    print(x,y,z,w)



answer ='wxzy'

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(2, 26, answer, 'd68899696c79e465e2a3547b4dc50435'))