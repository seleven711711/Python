nums = list(map(int, input().split()))
for n in range(1,len(nums)):
    if  nums[n]>nums[n-1]:
        print(nums[n], end=' ')
