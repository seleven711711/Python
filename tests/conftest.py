import hashlib
import os
import time
import sqlite3
import subprocess
import threading
from collections import defaultdict
from datetime import datetime

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap, ListedColormap
import matplotlib.patches as mpatches


def repo_root():
    # Корень репозитория — родительская папка для tests/
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Глобальный лок для операций Git, чтобы избежать конфликтов при параллельном доступе
git_lock = threading.Lock()

def git_add_file(file_path):
    """Добавляет файл в отслеживаемые Git."""

    with git_lock:
        try:
            if not os.path.exists(file_path):
                return False, f"Файл не найден перед git add: {file_path}"

            # Проверяем, находится ли файл в Git-репозитории
            git_dir = os.path.join(repo_root(), '.git')
            if not os.path.isdir(git_dir):
                return False, "Директория .git не найдена, возможно это не Git-репозиторий"

            # Используем относительный путь для git и заменяем слеши на прямые (для Windows)
            rel_path = os.path.relpath(file_path, repo_root())
            rel_path = rel_path.replace(os.sep, '/')

            # Выполняем команду git add для указанного файла
            result = subprocess.run(
                ['git', 'add', rel_path],
                cwd=repo_root(),  # Устанавливаем рабочую директорию в корень репозитория
                check=False,  # Не вызываем исключение при ошибке
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8', 
                errors='replace'
            )

            if result.returncode == 0:
                return True, "Файл успешно добавлен в отслеживаемые"
            else:
                return False, f"Ошибка при добавлении файла: {result.stderr}"
        except Exception as e:
            return False, f"Исключение при работе с Git: {str(e)}"


def git_commit(message="Автоматическое обновление статуса заданий"):
    """Создает коммит с указанным сообщением."""
    with git_lock:
        try:
            # Проверяем, находится ли файл в Git-репозитории
            git_dir = os.path.join(repo_root(), '.git')
            if not os.path.isdir(git_dir):
                return False, "Директория .git не найдена, возможно это не Git-репозиторий"
    
            # Выполняем команду git commit
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=repo_root(),  # Устанавливаем рабочую директорию в корень репозитория
                check=False,  # Не вызываем исключение при ошибке
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
    
            if result.returncode == 0:
                return True, "Коммит успешно создан"
            else:
                # Если нет изменений для коммита, это не ошибка
                if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                    return True, "Нет изменений для коммита"
                return False, f"Ошибка при создании коммита: {result.stderr}"
        except Exception as e:
            return False, f"Исключение при работе с Git: {str(e)}"


def rename_when_closed(src, dst, callback=None):
    """
    Пытается переименовать файл в отдельном потоке. 
    Если он занят, ждет 5 секунд и пробует снова, пока не освободится.
    """
    def _worker():
        while True:
            try:
                if os.path.exists(dst):
                    # Если целевой файл существует, удаляем его, чтобы rename сработал (как replace)
                    try:
                        os.remove(dst)
                    except OSError:
                        pass # Если не удалось удалить, возможно он тоже занят
                
                os.rename(src, dst)
                
                # Дополнительная проверка, что файл действительно переименовался
                if not os.path.exists(dst):
                     # Если файл не найден по новому пути, возможно произошел сбой, повторяем цикл
                     time.sleep(1)
                     continue

                if callback:
                    try:
                        callback()
                    except Exception as e:
                        print(f"Ошибка в callback после переименования: {e}")
                return
                
            except OSError: 
                # Файл занят. Ждем 5 секунд перед следующей попыткой
                time.sleep(3)

    thread = threading.Thread(target=_worker, daemon=False)
    thread.start()


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

def show_detailed_progress_table():
    """
    Создает таблицу, где:
    - По горизонтали расположены типы заданий (1-27)
    - По вертикали расположены даты решения
    - На пересечении отображаются номера заданий с цветовой индикацией правильности решения
    """
    results = get_results()

    if not results:
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.text(0.5, 0.5, "Нет данных для отображения", ha='center', va='center', fontsize=14)
        ax.set_axis_off()
        return fig

    # Группируем результаты по дате и типу задания
    # date -> task_type -> task_number -> result
    date_type_task_result = defaultdict(lambda: defaultdict(dict))

    # Собираем все уникальные даты и типы заданий
    all_dates = set()
    all_types = set()

    for dt, task_number, task_type, result in results:
        # Нормализация результата к 0/1
        try:
            r = int(result)
            r = 1 if r == 1 else 0
        except Exception:
            continue

        # Преобразуем дату в объект date
        date_only = None
        try:
            date_only = datetime.fromisoformat(str(dt)).date()
        except Exception:
            try:
                ts = float(dt)
                date_only = datetime.fromtimestamp(ts).date()
            except Exception:
                continue

        # Сохраняем только последний результат для каждого задания на каждую дату
        date_type_task_result[date_only][int(task_type)][int(task_number)] = r
        all_dates.add(date_only)
        all_types.add(int(task_type))

    # Сортируем даты и типы заданий
    sorted_dates = sorted(all_dates, reverse=True)  # Последние даты сверху
    sorted_types = sorted(all_types)  # Типы заданий по порядку

    # Создаем фигуру и оси
    # Мы не можем заранее знать высоту, поэтому сначала рассчитаем необходимые высоты строк
    
    # 1. Рассчитываем максимальное количество заданий в ячейке для каждой даты (строки)
    max_tasks_per_date = []
    for date in sorted_dates:
        max_t = 0
        for task_type in sorted_types:
            tasks = date_type_task_result[date].get(task_type, {})
            if len(tasks) > max_t:
                max_t = len(tasks)
        max_tasks_per_date.append(max(1, max_t)) # Минимум 1 слот высоты
        
    # Параметры отрисовки
    row_padding = 0.1  # Отступ между строками
    task_height = 0.34  # Высота одного блока задания
    task_gap = 0.06    # Зазор между блоками заданий
    
    # Рассчитываем координаты Y для каждой строки
    # y=0 будет вверху. Идем вниз.
    row_y_starts = []
    current_y = 0
    for count in max_tasks_per_date:
        row_height = count * task_height + row_padding
        row_y_starts.append((current_y, row_height))
        current_y -= row_height
        
    total_plot_height = abs(current_y)
    
    # Создаем фигуру с адаптивной высотой
    fig, ax = plt.subplots(figsize=(15, max(4, total_plot_height * 0.5)))
    
    # Настраиваем пределы осей
    ax.set_xlim(-0.5, len(sorted_types) - 0.5)
    ax.set_ylim(current_y, 0)
    
    # Рисуем сетку и данные
    for i, date in enumerate(sorted_dates):
        y_start, h = row_y_starts[i]
        y_center = y_start - h / 2
        
        # Горизонтальная линия разделителя (нижняя граница строки)
        ax.axhline(y_start - h, color='lightgray', linewidth=1)
        
        # Подпись даты слева
        ax.text(-0.6, y_center, date.strftime('%d.%m.%Y'), 
                ha='right', va='center', fontsize=9, fontweight='bold')
        
        # Рисуем данные по столбцам
        for j, task_type in enumerate(sorted_types):
            if task_type in date_type_task_result[date]:
                tasks = date_type_task_result[date][task_type]
                sorted_tasks = sorted(tasks.items())
                
                num_tasks = len(sorted_tasks)
                if num_tasks > 0:
                    # Рисуем блоки заданий
                    # Блоки занимают всю доступную ширину ячейки (1.0 минус отступы)
                    cell_width = 1.0
                    block_width = cell_width - 0.1 # Небольшой отступ по бокам
                    
                    # Начальный Y для первого блока в этой ячейке
                    # Отступ сверху внутри ячейки
                    cell_top = y_start - row_padding / 2
                    
                    for k, (task_num, res) in enumerate(sorted_tasks):
                        color = '#ccffcc' if res == 1 else '#ffcccc'
                        
                        # Границы слота
                        slot_bottom = cell_top - (k + 1) * task_height
                        
                        # Вычисляем высоту блока с учетом зазора
                        block_h = task_height - task_gap
                        # Центрируем блок в слоте (или сдвигаем, чтобы зазор был между блоками)
                        # Зазор разделим пополам сверху и снизу
                        block_y = slot_bottom + task_gap / 2
                        
                        # Рисуем прямоугольник
                        rect = mpatches.Rectangle(
                            (j - block_width/2, block_y), 
                            block_width, block_h,
                            facecolor=color, edgecolor='gray', linewidth=0.5
                        )
                        ax.add_patch(rect)
                        
                        # Текст (по центру блока)
                        symbol = "+" if res == 1 else "−"
                        txt = f"{symbol}{task_num}"
                        
                        # Текст выравниваем по центру вычисленного блока
                        text_x = j
                        text_y = block_y + block_h / 2
                        
                        ax.text(text_x, text_y, txt, 
                                ha='center', va='center', fontsize=8)

    # Вертикальные линии сетки
    for j in range(len(sorted_types) + 1):
        ax.axvline(j - 0.5, color='lightgray', linewidth=1)

    # Настраиваем оси X
    ax.set_xticks(np.arange(len(sorted_types)))
    ax.set_xticklabels([f"{t}" for t in sorted_types])
    ax.xaxis.set_tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
    
    # Убираем стандартные оси Y, так как мы их нарисовали вручную
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    # Добавляем заголовок и легенду
    ax.set_title("Детальный прогресс по заданиям", pad=20)

    # Настраиваем размер фигуры и отступы
    plt.tight_layout()

    return fig

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
        
        # Рассчитываем коэффициент на основе ВСЕ когда-либо решённых заданий данного типа
        # Считаем общее количество верно решённых заданий для данного типа из всех дат
        total_correct_count = 0
        for date_data in type_date_task_values[t].values():
            for vals in date_data.values():
                # Каждое задание (task_number) считается один раз, берём его максимальное значение
                if len(vals) > 0 and max(vals) == 1.0:
                    total_correct_count += 1
        
        # Применяем коэффициент на основе общего количества верно решённых заданий
        if total_correct_count < 10:
            coefficient = (total_correct_count * 10) / 100.0  # 10% за каждое верное задание
        else:
            coefficient = 1.0  # 100% для 10 и более
        
        percent = percent * coefficient
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

    # Вычисляем среднее арифметическое по всей диаграмме
    if percentages:
        mean_percentage = sum(percentages) / len(percentages)
        ax.text(0.95, 0.95, f'Среднее: {mean_percentage:.1f}',
                transform=ax.transAxes, ha='right', va='top', fontsize=12,
                bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

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
        extensions = ['.md', '.png', '.py', '.jpg', '.ods', '.xlsx', '.odt', '.docx', '.doc', '.xls', '.csv', '.txt']
        # Список найденных файлов
        files = []
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
                def on_rename_success():
                    # Пытаемся добавить в git ТОЛЬКО если файл реально существует и не занят
                    # Но поскольку git_add_file уже имеет проверки, просто вызываем его
                    success, message = git_add_file(dst)
                    if not success:
                        pass # print(f"Предупреждение при добавлении файла в Git: {message}")
                    
                    # Коммитим изменения СРАЗУ после успешного добавления файла
                    # Это гарантирует, что изменение статуса задания попадет в коммит
                    git_commit(f"Обновлен статус задания № {number} Тема: {task_type} > {('Верно' if res else 'Неверно')}")

                if os.path.abspath(src) != os.path.abspath(dst):
                    # Переименование в фоне
                    rename_when_closed(src, dst, callback=on_rename_success)
                else:
                    # Имя правильное, просто добавляем в git (если не добавлено)
                    on_rename_success()
                    
                renamed.append(dst)

            except Exception as e:
                print(f"Ошибка при переименовании файла: {str(e)}")

        return renamed

    mark_task_files(task_type, number, res == 1)
    fig = show_common_progress()
    fig_path = f'{repo_root()}/tests/common_progress.png'
    fig.savefig(fig_path)

    # Создаем и сохраняем детальную таблицу прогресса
    detail_fig = show_detailed_progress_table()
    detail_fig_path = f'{repo_root()}/tests/detailed_progress.png'
    detail_fig.savefig(detail_fig_path)

    # Добавляем график прогресса в Git и создаем коммит (для графиков отдельный коммит, если они изменились)
    git_add_file(fig_path)
    git_add_file(detail_fig_path)
    git_commit(f"Обновлены графики прогресса")
    
    return "Верно" if res else "Неверно"
