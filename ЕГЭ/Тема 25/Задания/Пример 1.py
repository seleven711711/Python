from fnmatch import fnmatch
for num in range(0,10**8,1991):
    if fnmatch(str(num),'3?1*57'):
        print(num,num//1991)