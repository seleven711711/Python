for a in range(11111):
    f = True
    for x in range(11111):
        if not (((x&5160>0) or (x&3650>0))<=((x&9545==0)<=(x&a>0))):
            f = False
            break
    if f:
         print(a)
         break
