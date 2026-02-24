from fnmatch import fnmatch
def get_divs(n):
    divs=set()
    for div in range(1,int(n**0.5)+1):
        if n%div==0:
            divs.add(div)
            divs.add(n//div)
    return divs


for num  in range(10**8,2*10**8):
    if fnmatch(str(num),'?*42*81'):
        if len(get_divs(num))==3:
            print(num)









