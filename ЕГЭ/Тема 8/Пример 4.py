from itertools import*
c = 0
for line in product("ВИЛМОС",repeat=5):
    line=''.join(line)
    c += 1
    if line.count('В')==1 and line.count('С')<=1 and line[0]!='О' and line[0]!='С' and c%2!=0:
        print(c)


