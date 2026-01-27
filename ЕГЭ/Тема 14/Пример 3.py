for x in '0123456789ABCDEFG':
    p1 = f'AB{x}12'
    p2 = f'4E{x}3F'
    r = int(p1, 17) + int(p2, 17)
    if r % 16 == 0:
        print(r // 8)
