# Решение
import itertools
from itertools import*
list_values=itertools.product('гепард',repeat=5)
count=0
for str in list_values:
    line=''.join(str)
    if line.count('г')==1 and line[0]!='а' and line[4]!='е':
        count+=1
        print(count)







answer =2200

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(8, 8, answer, '5249ee8e0cff02ad6b4cc0ee0e50b7d1'))