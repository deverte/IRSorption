import pandas as pd

"""
Модуль, содержащий функции, связанные с эквализацией (выравниванием) данных.
Используется для избавления от "плавания" температуры.
"""

def equalization_line(data, key, equilibrium_point):
    """
    Создание линии эквализации.
    Уравнение прямой с плавающей температурой является прямой с углом наклона,
    большим, чем 0 градусов. Таким образом, она выражается следующим равенством:
    y_float = kx = [y(f) - y(0)] / N * x, где а - время в конце, N - количество
    измерений. В итоге, нам нужна прямая без наклона: y_0 = e, где e - точка
    сдвига равновесия, относительно которой будет строиться линия эквализации.
    Следовательно, для перехода к такой прямой, линия эквализации будет
    записываться в виде: y_eq = y_float + y_0 = [y(f) - y(0)] / N * x + e.

    Параметры:
        data - таблица данных, которые нужно выровнять. Тип - pandas.DataFrame.
        key - индекс столбца, для которого строится линия эквализации.
    Тип - str.
        equilibrium_point - точка сдвига равновесия. Тип - float.

    Возвращает линию эквализации. Тип - pandas.DataFrame.
    """
    # Создаём таблицу для линии эквализации
    line = pd.DataFrame(index=data.index)
    line_tuple = [] # Временный список для хранения данных линии эквализации
    # Вычисляем сдвиг - вычитаем из точки сдвига равновесия минимальную из
    # границ.
    shift = equilibrium_point - min(data[key].iloc[-1], data[key].iloc[0])
    # Строим линию эквализации
    # k = [y(f) - y(0)] / N
    k = (data[key].iloc[-1] - data[key].iloc[0]) / len(data[key])
    for x in range(len(data.index)):
        # Строим линию: y_eq = kx + e
        line_tuple.append(k * (x + 1) + shift) # x + 1, т.к. kx != 0
    line["equalization_line"] = line_tuple
    return line

def equalization(data, equilibrium_points):
    """
    Эквализация данных.

    Параметры:
        data - таблица данных, которые нужно выровнять. Тип - pandas.DataFrame.
        equilibrium_points - точки сдвига равновесия. Для каждого столбца нужно
    использовать свою точку равновесия, т.к. у каждой кривой должна быть своя
    линия эквализации. Тип - dict[str: float].

    Возвращает таблицу выровненных данных. Тип - pandas.DataFrame.
    """
    # Создаём таблицу для эквализованных данных
    equalized = pd.DataFrame(index=data.index)
    # Эквализуем каждый столбец
    for key in data.keys():
        # Получим индекс столбца
        point = equilibrium_points[key]
        # Построим линию эквализации для столбца
        eq_line = equalization_line(data, key, point)["equalization_line"]
        # Сдвинем столбец на линию эквализации
        equalized[key] = data[key] - eq_line
    return equalized
