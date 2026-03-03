def f(n):
    if n==0:
        return 0
    elif n%2==0 and n>0:
        return f(n//10)+n%10
    elif n%2!=0:
        return f(n//10)
i=0
for n in range (10**7,6*10**7):
    if f(n)==0:
        i+=1
print(i)

