import pandas as pd
import numpy as np

"""
Модуль, содержащий функции, связанные с взятия производных.
"""

def derivative(data):
    """
    Функция взятия производной по каждому столбцу данных.

    Параметры:
        data - таблица данных, которые нужно продифференцировать.
    Дифференцирование проходит по индексам (обычно индексы - это время).
    Тип - pandas.DataFrame.

    Возвращает производную от данных. Тип - pandas.DataFrame.
    """
    # Создаём таблицу для производных
    derivatives = pd.DataFrame(index=data.index)
    # Дифференцируем каждый столбец
    for key in data.keys():
        derivatives[key] = np.gradient(data[key])
    return derivatives
