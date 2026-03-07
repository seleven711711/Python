# Решение255.255.254.0
# 255.255.248.0
# 255.255.252.0

from ipaddress import ip_network
network = ip_network('157.220.185.237')
count=0
for ip in ip_network('157.220.185.237/255.255.254.0',False):
    if f'{ip:b}'.count('1') == 15:
        count+=1
print(count)
answer = 9

#

from tests.conftest import result_register
if answer is not Ellipsis:
    print(result_register(13, 1301, answer, '45c48cce2e2d7fbdea1afc51c7c6ad26'))