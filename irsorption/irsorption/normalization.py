import pandas as pd
import numpy as np

"""
Модуль, содержащий функции, связанные с нормировкой данных (сдвиг всех столбцов
к одним начальным данным [температуре]).
"""

def normalize(data, begin, end):
    """
    Нормировка данных.

    Параметры:
        data - таблица данных, которые нужно нормировать.
    Тип - pandas.DataFrame.
        begin - индекс (момент времени) начала отрезка, при котором должны быть
    одинаковые данные [температуры]. Тип - float.
        end - индекс (момент времени) конца отрезка нормировки. Тип - float.

    Возвращает нормированные данные. Тип - pandas.DataFrame.
    """
    # Выделяем данные заданного интервала
    data = data[begin:end]
    # Создаём таблицу для нормированных данных
    normalized = pd.DataFrame(index=data.index)
    # Получаем данные [температуры] в момент времени begin по каждому столбцу.
    inits = []
    for key in data.keys():
        inits.append(data[key].iloc[0])
    # Усредняем данные в момент begin.
    mean = np.mean(inits)
    # Нормируем (сдвигаем) данные
    for key in data.keys():
        # Вычисляем сдвиг для каждого столбца
        shift = data[key].iloc[0] - mean
        # Сдвигаем каждый столбец
        normalized[key] = data[key] - shift
    return normalized
