def game(heap, moves, to):
    if heap <= 30:
        return moves % 2 == to % 2
    if moves == to:
        return 0
    h = [game(heap - 3, moves + 1, to),
         game(heap - 5, moves + 1, to),
         game(heap // 4, moves + 1, to)]
    return any(h) if (moves + 1) % 2 == to % 2 else all(h)

print(f'19: {min(s for s in range(1000, 30, -1) if not game(s, 0, 1) and game(s, 0, 2))}')
print(f'20: {[s for s in range(1000, 30, -1) if not game(s, 0, 1) and game(s, 0, 3)][-2:]}')
print(f'20: {min(s for s in range(1000, 30, -1) if not game(s, 0, 2) and game(s, 0, 4))}')