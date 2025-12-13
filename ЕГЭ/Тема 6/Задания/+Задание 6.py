# Решение
from turtle import*
tracer(0)
k=20
lt(90)
down()
for i in range(2):
    fd(3*k)
    lt(90)
    backward(10*k)
    lt(90)
up()
backward(10*k)
rt(90)
fd(8*k)
lt(90)
down()
for i in range(2):
    fd(16*k)
    rt(90)
    fd(8*k)
    rt(90)
up()
for x in range(-20,20):
    for y in range(-20,20):
        goto(x*k,y*k)
        dot(4)
exitonclick()










answer =185

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(6, 6, answer, 'eecca5b6365d9607ee5a9d336962c534'))