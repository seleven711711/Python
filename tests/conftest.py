import hashlib
import os
import sqlite3
from datetime import datetime

from matplotlib import pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap


def repo_root():
    # Корень репозитория — родительская папка для tests/
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def db_path():
    # БД всегда в tests/result.db относительно корня репозитория
    return os.path.join(repo_root(), 'tests', 'result.db')


def create_new_db():
    os.makedirs(os.path.dirname(db_path()), exist_ok=True)
    with sqlite3.connect(db_path()) as connection:
        cursor = connection.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS test (
                                                           date_time   DATETIME,
                                                           task_number BIGINT,
                                                           task_type   INTEGER,
                                                           result      INTEGER
                       )
                       ''')


def add_result(date_time, task_number, task_type, result):
    if not os.path.exists(db_path()):
        create_new_db()
    with sqlite3.connect(db_path()) as connection:
        cursor = connection.cursor()
        # Проверяем, есть ли уже запись с таким task_number и task_type
        existing = get_result(task_number, task_type)
        
        # Если запись существует и последний результат был правильным (1), не добавляем новую запись
        if existing and existing[3] == 1:
            return  # Не добавляем дубликат правильного ответа
        
        # В остальных случаях добавляем новую запись
        cursor.execute('INSERT INTO test (date_time, task_number, task_type, result) VALUES (?, ?, ?, ?)',
                       (date_time, task_number, task_type, result))


def update_result(date_time, task_number, task_type, result):
    with sqlite3.connect(db_path()) as connection:
        cursor = connection.cursor()
        cursor.execute('UPDATE test SET date_time = ?, result = ? WHERE task_type = ? AND task_number = ?',
                       (date_time, result, task_type, task_number))


def get_result(task_number, task_type):
    with sqlite3.connect(db_path()) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM test WHERE task_number = ? AND task_type = ?',
                       (task_number, task_type))
        return cursor.fetchone()


def get_results():
    with sqlite3.connect(db_path()) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM test')
        return cursor.fetchall()


def show_common_progress():
    """
    Получить из БД все разультаты и сгруппировать их по полю task_type.
    Для каждого типа посчитать процент правильных ответов среди всех решенных заданий данного типа,
    в подсчёт включаются только данные за последние 5 дат.
    При этом необходимо находить среднее значение по каждому номеру задания (task_number).
    Построить гистограмму, где на оси X будут номера тем, а на Y — процент правильных ответов.
    """
    from collections import defaultdict

    results = get_results()

    # type -> date -> task_number -> list[result]
    type_date_task_values = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for dt, task_number, task_type, result in results:
        # Нормализация результата к 0/1, некорректные значения/строки пропускаем
        try:
            r = int(result)
            r = 1 if r == 1 else 0
        except Exception:
            continue

        # Преобразуем дату в объект date (сначала ISO, затем timestamp для обратной совместимости)
        date_only = None
        try:
            date_only = datetime.fromisoformat(str(dt)).date()
        except Exception:
            try:
                ts = float(dt)
                date_only = datetime.fromtimestamp(ts).date()
            except Exception:
                continue

        type_date_task_values[int(task_type)][date_only][int(task_number)].append(r)

    # Считаем процент по каждому типу: берём последние 5 дат, считаем среднее по каждому task_number,
    # затем усредняем по task_number и переводим в проценты
    x_types = list(range(1, 28))  # 1..27
    percentages = []

    for t in x_types:
        date_map = type_date_task_values.get(t, {})
        if not date_map:
            percentages.append(0.0)
            continue

        last_dates = sorted(date_map.keys(), reverse=True)[:5]
        if not last_dates:
            percentages.append(0.0)
            continue

        task_to_values = defaultdict(list)
        for d in last_dates:
            for task_num, vals in date_map[d].items():
                task_to_values[task_num].extend(vals)

        if not task_to_values:
            percentages.append(0.0)
            continue

        per_task_means = []
        for vals in task_to_values.values():
            if len(vals) > 0:
                per_task_means.append(sum(vals) / len(vals))

        percent = (sum(per_task_means) / len(per_task_means)) * 100 if per_task_means else 0.0
        percentages.append(percent)

    # Построение гистограммы
    fig, ax = plt.subplots(figsize=(12, 5))
    norm = Normalize(vmin=0, vmax=100)
    # Цветовая схема
    cmap = LinearSegmentedColormap.from_list("red_green", ["red", "orange", "green"])
    colors = cmap(norm(percentages))
    bars = ax.bar(x_types, percentages, color=colors)
    # ---
    for bar, val in zip(bars, percentages):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2,
                f"{val:.1f}", ha='center', va='center', color='black')

    ax.set_xlabel('Номер темы')
    ax.set_ylabel('Показатель успеваемости')
    ax.set_title('Общий прогресс')
    ax.set_xticks(x_types)
    ax.set_ylim(0, 100)

    return fig

def result_register(task_type, number, result, right_result):
    """
    Помечать файл задания, добавляя к имени файла в начало '+' или '-', соответственно.
    Оперделение пути файла проиходится через переменные task_type и number.
    Файлы располагаются в подпапке: Тема {task_type}/Задания/
    Имя файла: "Задание {number}.md" или "Задание {number}.png".
    """
    res = 1 if hashlib.md5(str(result).encode()).hexdigest() == right_result else 0
    # Храним дату в читабельном ISO-формате
    add_result(datetime.now().isoformat(), number, task_type, res)

    def mark_task_files(task_type, number, is_correct):
        """Ищет файлы задания (.md и .png и пр.) и переименовывает, добавляя префикс '+' или '-'"""
        try:
            t = int(task_type)
            n = int(number)
        except Exception:
            return []

        # Строим путь относительно корня репозитория, отталкиваясь от текущего файла tests/conftest.py
        task_dir = os.path.join(repo_root(), f"Тема {t}", "Задания")

        if not os.path.isdir(task_dir):
            task_dir = os.path.join(repo_root(), "ЕГЭ", f"Тема {t}", "Задания")
        if not os.path.isdir(task_dir):
            return []

        # Список поддерживаемых расширений файлов
        extensions = ['.md', '.png', '.py', '.jpg', '.ods', '.xlsx']
        sign = '+' if is_correct else '-'
        renamed = []

        for ext in extensions:
            base_name = f"Задание {n}{ext}"
            # Кандидаты: без префикса и с обоими префиксами
            candidates = [
                os.path.join(task_dir, base_name),
                os.path.join(task_dir, '+' + base_name),
                os.path.join(task_dir, '-' + base_name),
            ]

            src = None
            for cand in candidates:
                if os.path.exists(cand):
                    src = cand
                    break
            if not src:
                continue

            dst = os.path.join(task_dir, sign + base_name)
            try:
                if os.path.abspath(src) != os.path.abspath(dst):
                    os.replace(src, dst)  # перезаписываем, если существует файл с другим префиксом
                renamed.append(dst)
            except Exception:
                # Игнорируем ошибки переименования, чтобы не ронять тесты
                pass

        return renamed

    mark_task_files(task_type, number, res == 1)
    fig = show_common_progress()
    fig.savefig(f'{repo_root()}/tests/common_progress.png')
    return "Верно" if res else "Неверно"