a = int(input())
b = int(input())
c = int(input())
k1 = min(a, b, c)
h = max(a, b, c)
k2 = a + b + c - (h + k1)
if k1 + k2 <= h:
    print('Не существует')
elif k1 ** 2 + k2 ** 2 == h ** 2:
    print('Прямоугольный')
elif k1 ** 2 + k2 ** 2 < h ** 2:
    print('Остроугольный')
elif k1 ** 2 + k2 ** 2 > h ** 2:
    print('Тупоугольный')
