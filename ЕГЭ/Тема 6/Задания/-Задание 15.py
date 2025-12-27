# Решение
from turtle import*
k=20
tracer(0)
for i in range(4):
    fd(14*k)
    rt(90)
for i in range(5):
    fd(5*k)
    rt(45)
up()
for x in range(-20,20):
    for y in range(-20,20):
        goto(x*k,y*k)
        dot(3)
exitonclick()







answer =67

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(6, 15, answer, '093f65e080a295f8076b1c5722a46aa2'))