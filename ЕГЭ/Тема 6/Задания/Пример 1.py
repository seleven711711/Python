from turtle import *
tracer(0)
koef=27
for i in range(5):
    forward(2*koef)
    right(90)
    forward(3*koef)
up()
for x in range(-koef,koef):
    for y in range(-koef,koef):
        goto(x*koef,y*koef)
        dot(3)
exitonclick()
for x in range(20):
    if (x+4)**2 > 400:
        print(x)
