# Решение
from turtle import*
tracer(0)
k=10
screensize(3000, 3000)
rt(180)
for i in range(9):
    fd(59*k)
    lt(90)
    fd(84*k)
    lt(90)
up()
fd(18*k)
rt(90)
fd(38*k)
rt(90)
down()
for i in range(9):
    fd(120*k)
    rt(90)
    fd(99*k)
    rt(90)
up()
for x in range(-100,100):
    for y in range(-100,100):
        goto(x*k,y*k)
        dot(3)
exitonclick()







answer =158

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(6, 62, answer, '06409663226af2f3114485aa4e0a23b4'))