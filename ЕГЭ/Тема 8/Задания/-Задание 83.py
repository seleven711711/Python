# Решение
from itertools import*
c=0
for line in product('бкфц',repeat=5):
    line=''.join(line)
    c+=1
print(c)











answer = 'бцфцф'

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(8, 83, answer, 'f0a551e113a7af86f780ae14e74c3ac7'))