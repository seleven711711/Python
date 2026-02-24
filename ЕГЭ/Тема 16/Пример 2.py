def f(n):
    if n<5000:
        return n
    elif n>=5000 and n%5==0:
        return n+f(n//5)
    elif n>=5000 and n%5!=0:
        return 117+f(n-3)
for n in range(1,100000):
    if f(n)>100000:
        print(n)
