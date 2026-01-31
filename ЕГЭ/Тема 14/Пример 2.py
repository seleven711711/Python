for x in '0123456789ABCDE':
    p1 = f'98{x}79641'
    p2 = f'25{x}49'
    p3 = f'63{x}5'
    r = int(p1, 22) + int(p2, 22) + int(p3, 22)
    if r % 21 == 0:
        print(r // 21)
        break
