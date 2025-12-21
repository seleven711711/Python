from itertools import*
count = 0
for line in permutations('РУСЛАН'):
    line=''.join(line)
    if line.count('АУ')==0 and line.count('УА')==0:
        count += 1
print(count)

