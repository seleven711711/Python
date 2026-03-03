# Решение
from turtle import*
k=20
tracer(0)
screensize(2000,2000)
for n in range(2):
    fd(23*k)
    rt(90)
    fd(10*k)
    rt(90)
fd(3*k)
lt(90)
fd(12*k)
rt(90)
for n in range(2):
    fd(9*k)
    rt(90)
    fd(32*k)
    rt(90)
up()
for x in range(-60,60):
    for y in range(-60,60):
        goto(x*k,y*k)
        dot(3)
exitonclick()









answer =110

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(6, 65, answer, '5f93f983524def3dca464469d2cf9f3e'))