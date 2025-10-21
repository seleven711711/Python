n = int(input())
for i in range(1000):
    if n % 10 == 1 and n % 100 != 11:
        print('гриб')
    elif 1 < n % 10 < 5 and n % 100 < 12:
        print('гриба')
    else:
        print('грибов')
