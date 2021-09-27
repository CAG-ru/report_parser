import numpy as np
import pandas as pd
from bs4.element import NavigableString, Comment, Doctype

from report_parser.src.text_class import Text


def print_tag(tag):
    print('printing tag:', type(tag), tag.name)
    if type(tag) not in [NavigableString, Doctype, Comment]:
        for child in tag.children:
            print('child:', type(child), child.name)


def get_texts_and_tables(html_elems, new_method):
    contents = []
    contents_num = len(html_elems)
    cur_elem_num = 0

    while cur_elem_num < contents_num:
        elem_type, elem = html_elems[cur_elem_num]
        accumulated_texts = []
        table = None

        while elem_type == 'text' and cur_elem_num < contents_num:
            accumulated_texts.append(elem)
            cur_elem_num += 1
            if cur_elem_num < contents_num:
                elem_type, elem = html_elems[cur_elem_num]

        if len(accumulated_texts):
            contents.append(Text(accumulated_texts))
            accumulated_texts = []

        if elem_type == 'table':
            # TODO: временная мера для тестирования нового метода
            if new_method:
                table = parse_table_new(elem)
            else:
                table = parse_table(elem)
            if table.shape[0]:
                contents.append(table)

        cur_elem_num += 1
    return contents


def parse_table_new(table_rows):
    """
    Парсинг таблиц, полученныхых в результате работы ParsingTree
    """
    df = pd.DataFrame()
    for i in range(len(table_rows)):
        html_row = table_rows[i]

        row = [x for x in html_row]
        # Пропускаем пустые строки:
        if not any([x[2] for x in row]):
            continue
        flatten_row = []
        # Смотрим на значения каждой ячейки в строке
        for col_index in range(len(row)):
            row_span = row[col_index][0]
            col_span = row[col_index][1]
            value = row[col_index][2]

            # Заполняем ячейки ниже значениями текущей ячейки
            if row_span > 1:
                # Берём нужное количество строк, начиная с текущей,
                # и в нужный индекс вставляем значение с row_span == 1
                for _ in range(row_span):
                    real_index = sum([x[1] for x in row][:col_index])
                    cell_value = (1, col_span, value)
                    table_rows[i + _].insert(real_index, cell_value)

            # Копируем значение ячейки в несколько следующих столбцов (или нет)
            if col_span == 1:
                flatten_row.append(value)
            else:
                flatten_row.extend([value] * col_span)
        # Добавляем список значений строки в датафрейм
        df = df.append([flatten_row])
    df.reset_index(inplace=True, drop=True)
    return df


def parse_table(table_rows):
    max_col_num = get_max_colspan(table_rows)

    df = pd.DataFrame(columns=range(max_col_num), dtype=str)

    col_shifts = [0]
    row_shift = 0

    for i in range(len(table_rows)):
        html_row = table_rows[i]
        df_len = len(df)

        cur_shift = col_shifts.pop() if col_shifts else 0

        if row_shift == 0:
            # if True:
            df.append(pd.Series(dtype=str), ignore_index=True)

        next_row_shift = 0

        for j in range(len(html_row)):

            cell = html_row[j]
            shape = (cell[0], cell[1])

            need_rows = shape[0] - (len(df) - df_len)
            next_row_shift = max(need_rows - 1, next_row_shift)

            for _ in range(need_rows - 1):
                df.append(pd.Series(dtype=str), ignore_index=True)
                col_shifts.append(cur_shift + shape[1])

            for cell_row_n, cell_col_n in np.ndindex((shape[0], shape[1])):
                row = df_len - row_shift + cell_row_n
                col = cur_shift + cell_col_n
                df.loc[row, col] = cell[2]

            cur_shift += shape[1]

        if row_shift:
            row_shift -= 1
        row_shift = row_shift + next_row_shift

    return df


def get_max_colspan(table_rows):
    max_col_num = 0
    for row in table_rows:
        col_num = 0
        for cell in row:
            col_num += cell[1]
        max_col_num = max(max_col_num, col_num)
    return (max_col_num)
