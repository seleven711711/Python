from itertools import product

s = product('1234', repeat=2)
for line in s:
    print(''.join(line))

print()

for i in '1234':
    for j in '1234':
        print(f'{i}{j}')