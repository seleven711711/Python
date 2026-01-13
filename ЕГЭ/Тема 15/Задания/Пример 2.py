p = range(12,62)
q = range(32,92)
min_len=100
for begin in range(100):
    for end in range(100):
        a=range(begin,end)
        for x in range(100):
            if not((not(x in a) and (x in q)) <= (x in p)):
                break
        else:
            min_len = min(min_len, end - begin)
print(min_len)

