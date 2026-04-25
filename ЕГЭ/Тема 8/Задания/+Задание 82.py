# Решение
from itertools import*
c=0
for line in product('акорст',repeat=5):
    line=''.join(line)
    c += 1
    if line[0]!='а' and line[0]!='с' and line[0]!='т' and line.count('о')==2 and c%2==0:
        print(c)













answer = 5058

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(8, 82, answer, '7ffb4e0ece07869880d51662a2234143'))