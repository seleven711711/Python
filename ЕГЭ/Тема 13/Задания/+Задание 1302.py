# Решение
from ipaddress import ip_network
count=0
for ip in ip_network('122.159.136.144/255.255.255.248',False):
    if f'{ip:b}'.count('1')%4!=0:
        count+=1
print(count)







answer =5

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(13, 1302, answer, 'e4da3b7fbbce2345d7772b0674a318d5'))