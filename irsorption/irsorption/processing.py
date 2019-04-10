import pandas as pd
import numpy as np

from .smooth import smooth
from .equalization import equalization
from .derivative import derivative
from .normalization import normalize
from .integration import integrate
from .ia import interval_analysis

"""
Модуль, предназначенный для обработки файла с настройками.
"""

"""
TODO:
1. В функции do_equalization добавить выбор точки эквализации (в процентах).
"""

def processing(fileName):
    """
    Обработка данных по заданному плану.

    Параметры:
        fileName - имя файла с планом. Тип - str.
    """
    # Считываем файл в таблицу DataFrame
    settings = pd.read_csv(fileName, index_col=0)
    # Проходимся по каждой строке и в зависимости от команды, выполняем функции
    for i in range(len(settings)):
        if settings.index[i] == "smooth":
            print("[{}/{}]: {}".format(i + 1, len(settings), "smooth"))
            # Считываем значения в полях N и Wn. Если их нет, то устанавливаем
            # значения по умолчанию
            N = settings.iloc[i]["N"]
            if np.isnan(N):
                N = 3
            Wn = settings.iloc[i]["Wn"]
            if np.isnan(N):
                N = 1e-3
            # Выполняем сгладивание
            do_smooth(settings.iloc[i]["fileIn"], settings.iloc[i]["fileOut"],
                      N = N, Wn = Wn)
        elif settings.index[i] == "equalization":
            print("[{}/{}]: {}".format(i + 1, len(settings), "equalization"))
            do_equalization(settings.iloc[i]["fileIn"],
                            settings.iloc[i]["fileOut"])
        elif settings.index[i] == "derivative":
            print("[{}/{}]: {}".format(i + 1, len(settings), "derivative"))
            do_derivative(settings.iloc[i]["fileIn"],
                          settings.iloc[i]["fileOut"])
        elif settings.index[i] == "normalization":
            print("[{}/{}]: {}".format(i + 1, len(settings), "normalization"))
            do_normalization(settings.iloc[i]["fileIn"],
                             settings.iloc[i]["fileOut"])
        elif settings.index[i] == "ia":
            print("[{}/{}]: {}".format(i + 1, len(settings), "ia"))
            do_ia(settings.iloc[i]["fileIn"], settings.iloc[i]["directory"],
                  settings.iloc[i]["begin"], settings.iloc[i]["end"],
                  settings.iloc[i]["mode"], settings.iloc[i]["extrema"])

def do_smooth(fileIn, fileOut, N=3, Wn=1e-3):
    """
    Сглаживание с использованием фильтра Баттерворта.

    Параметры:
        fileIn - имя входного файла. Тип - str.
        fileOut - имя выходного файла. Тип - str.
        N - порядок фильтра (точность). Тип - int.
        Wn - частота Найквиста (половина частоты дискретизации сигнала).
    Тип - float.
    """
    data = pd.read_csv(fileIn, index_col=0, dtype=np.double)

    smoothed = pd.DataFrame(index=data.index)
    for key in data.keys():
        smoothed[key] = smooth(data[key], N, Wn)[0]

    smoothed.to_csv(fileOut)

def do_equalization(fileIn, fileOut):
    """
    Эквализация (выравнивание) сигнала.

    Параметры:
        fileIn - имя входного файла. Тип - str.
        fileOut - имя выходного файла. Тип - str.
    """
    data = pd.read_csv(fileIn, index_col=0, dtype=np.double)

    ep = {}
    for key in data.keys():
        ep[key] = (data[key].iloc[0] + data[key].iloc[-1]) / 2

    equalized = equalization(data, ep)

    equalized.to_csv(fileOut)

def do_derivative(fileIn, fileOut):
    """
    Численное дифференцирование.

    Параметры:
        fileIn - имя входного файла. Тип - str.
        fileOut - имя выходного файла. Тип - str.
    """
    data = pd.read_csv(fileIn, index_col=0, dtype=np.double)

    derivatives = derivative(data)

    derivatives.to_csv(fileOut)

def do_normalization(fileIn, fileOut):
    """
    Нормировка сигнала.

    Параметры:
        fileIn - имя входного файла. Тип - str.
        fileOut - имя выходного файла. Тип - str.
    """
    data = pd.read_csv(fileIn, index_col=0, dtype=np.double)

    normalized = normalize(data, 100, 600)

    normalized.to_csv(fileOut)

def do_ia(fileIn, directory, begin, end, mode, extrema):
    """
    Интервальный анализ (поиск экстремумов, интегралов, производных).

    Параметры:
        fileIn - имя входного файла. Тип - str.
        directory - название директории, в которую будут сохраняться
    интервальные данные. Тип - str.
        begin - индекс (момент времени) начала отрезка. Тип - float.
        end - индекс (момент времени) конца отрезка. Тип - float.
        mode - режим анализа. Зависит от того, информацию о скольки точках нужно
    получить. Тип - int.
    Может принимать значения:
    2 - две точки: начальная и конечная. Вид экстремума не влияет.
    3 - три точки: начальная, экстремум и конечная. Вид экстремума определяется
    для точки экстремума.
        extrema - вид экстремума. Есть смысл указывать только для трёх точек.
    Тип - str.
    Может принимать значения:
    "min" - минимум.
    "max" - максимум.
    """
    data = pd.read_csv(fileIn, index_col=0, dtype=np.double)

    interval_analysis(data, begin, end, mode=mode, extrema=extrema,
                                 output="Write", directory=directory)
