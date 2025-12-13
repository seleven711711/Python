## Библиотека itertools

Функции библиотеки:

> <code>product(множество, [repeat=кол_во_повторений_множества])</code>\
> Возвращает декартово произведение множеств.

> <code>combinations(множество, длина)</code>\
> Возвращает комбинации из элементов, длина которых указана во втором параметре.\
> Комбинации составляются из элементов, отсортированных лексикографически (по алфавиту).

> <code>permutations(множество, [длина_элемента])</code>\
> Возвращает перестановки элементов, длина которых указана в параметре.\
> Элементы множества не повторяются. \
> Если длина не указана, то размер элементов равен размеру множества.

> <code>combinations_with_replacement(множество, длина_элемента)</code>\
> Функция похожа на обычный <code>combinations</code>, но значения в элементах повторяются.

<br>
<table class="docutils align-default">
    <thead>
        <tr class="row-odd">
            <th class="head">Пример</th>
            <th class="head">Результат работы</th>
        </tr>
    </thead>
    <tbody>
        <tr class="row-even"><td><code><span>product('ABCD',</span> <span >repeat=2)</span></code></td>
        <td><code><span>AA</span> <span >AB</span> <span >AC</span> <span >AD</span> <span >BA</span> <span >BB</span> <span >BC</span> <span >BD</span> <span >CA</span> <span >CB</span> <span >CC</span> <span >CD</span> <span >DA</span> <span >DB</span> <span >DC</span> <span >DD</span></code></td>
        </tr>
        <tr class="row-odd"><td><code ><span >permutations('ABCD',</span> <span >2)</span></code></td>
        <td><code ><span >AB</span> <span >AC</span> <span >AD</span> <span >BA</span> <span >BC</span> <span >BD</span> <span >CA</span> <span >CB</span> <span >CD</span> <span >DA</span> <span >DB</span> <span >DC</span></code></td>
        </tr>
        <tr class="row-even"><td><code ><span >combinations('ABCD',</span> <span >2)</span></code></td>
        <td><code ><span >AB</span> <span >AC</span> <span >AD</span> <span >BC</span> <span >BD</span> <span >CD</span></code></td>
        </tr>
        <tr class="row-odd"><td><code ><span >combinations_with_replacement('ABCD',&nbsp;2)</span></code></td>
        <td><code ><span >AA</span> <span >AB</span> <span >AC</span> <span >AD</span> <span >BB</span> <span >BC</span> <span >BD</span> <span >CC</span> <span >CD</span> <span >DD</span></code></td>
        </tr>
    </tbody>
</table>
<br>