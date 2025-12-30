"""
На числовой прямой даны два отрезка: Р = [12, 62] и Q = [52, 92]. Какова наименьшая возможная длина интервала A, что логическое выражение

                                        ¬(¬(х ∈ А) ∧ (х ∈ Р)) ∨ (х ∈ Q)

тождественно истинно, то есть принимает значение 1 при любом значении переменной х.
Ответ: 40
"""

p = range(12, 62)
q = range(52, 92)
min_len = 100
for begin in range(100):
    for end in range(100):
        a = range(begin, end)
        if all(not (not(x in a) and (x in p)) or (x in q) for x in range(100)):
            min_len = min(min_len, end - begin)
print(min_len)