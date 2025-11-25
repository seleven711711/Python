start_sum = float(input())
target_sum = float(input())
percent = float(input())
m = 0
percent = percent  / 12
while start_sum < target_sum:
    start_sum = start_sum + start_sum  *  percent / 100
    m += 1
    print(f'{m} - {start_sum}')
