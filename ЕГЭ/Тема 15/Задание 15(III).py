"""
Для какого наименьшего целого неотрицательного числа А выражение

            (x + 2y < A) ∨ (y > x) ∨ (x > 60)

тождественно истинно (то есть принимает значение 1) при любых целых неотрицательных х и y?
"""

for a in range(400):
    f = True
    for x in range(400):
        for y in range(400):
            if not ((x + 2 * y < a) or (y > x) or (x > 60)):
                f = False
    if f:
        print(a)
        break

'''
# Альтернативное решение
for a in range(400):
    if all((x + 2 * y < a) or (y > x) or (x > 60) for x in range(400) for y in range(400)):
        print(a)
        break
'''