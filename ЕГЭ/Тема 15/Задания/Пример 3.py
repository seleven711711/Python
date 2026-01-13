for a in range(1000):
    f = True
    for x in range(1000):
        for y in range(1000):
            if not((x>=9) or (2*x<y) or (x*y<a)):
                f = False
    if f:
        print(a)
        break