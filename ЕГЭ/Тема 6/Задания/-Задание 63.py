# Решение
from turtle import*
k=7
tracer(0)
screensize(3000,3000)
for n in range(7):
    fd(17*k)
    rt(90)
    fd(26*k)
    rt(90)
up()
fd(4*k)
rt(90)
fd(6*k)
lt(90)
down()
for n in range(7):
    fd(278*k)
    rt(90)
    fd(345*k)
    rt(90)
up()
for x in range(-50,50):
    for y in range(-50,50):
        goto(x*k,y*k)
        dot(3)
exitonclick()








answer =280

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(6, 63, answer, '35495f83adcdab84ab446b313a3e0cb4'))