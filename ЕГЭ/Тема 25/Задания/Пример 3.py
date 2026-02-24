from fnmatch import fnmatch
for num in range(0,10**10,2026):
    if fnmatch(str(num),'7?23?64*8')and str(num)[1] in '02468'and str(num)[4] in '02468' :
        print(num)

