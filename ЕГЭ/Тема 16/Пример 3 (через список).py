nums = [0] * 100000000

for n in range(0, 100000000):
    if n == 0:
        nums[n] = 0
    elif n > 0 and n % 2 == 0:
        nums[n] = nums[n // 10] + n % 10
    elif n % 2 != 0:
        nums[n] = nums[n // 10]
count = 0
for n in range(10 ** 7, 6 * 10 ** 7 + 1):
    if nums[n] == 0:
        count += 1
print(count)