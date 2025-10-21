n = int(input())
if n % 10 == 1 and n %100 != 11:
    print('гриб')
elif 1 < n % 10 < 5 and 14<n<11:
    print('гриба')
else:
    print('грибов')
