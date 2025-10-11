from math import sqrt

x1 = int(input())
y1 = int(input())
x2 = int(input())
y2 = int(input())
x3 = int(input())
y3 = int(input())
a = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
b = sqrt((x3 - x2) ** 2 + (y3 - y2) ** 2)
c = sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)
p = (a+b+c)/2
print(f"Площадь= {sqrt(p*(p-a)*(p-b)*(p-c))}")
