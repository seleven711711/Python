# Решение
p=range(19,84)
q=range(4,51)
min_len = 100
for begin in range (100):
    for end in range (100):
        a = range(begin, end)
        if all ((x in q)<= ((x not in p)<= (not ((x in q) and  (x not in a)))) for x in range(100)):
            min_len=min(min_len,end-begin)
print(min_len)








answer =15

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(15, 152, answer, '9bf31c7ff062936a96d3c8bd1f8f2ff3'))