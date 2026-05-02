# Решение
from itertools import*
c=0
g='ОА'
s='РСМХ'
for line in product(g,s,g,s,g,s,g,s):
    line=''.join(line)
    if line.count('О')==2 and line.count('А')==2 and line.count('Р')==1 and line.count('С')==1 and line.count('М')==1 and line.count('Х')==1:
        c+=1
for line in product(s,g,s,g,s,g,s,g):
    line=''.join(line)
    if line.count('О')==2 and line.count('А')==2 and line.count('Р')==1 and line.count('С')==1 and line.count('М')==1 and line.count('Х')==1:
        c+=1
print(c)







answer = 288

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(8, 81, answer, '48aedb8880cab8c45637abc7493ecddd'))