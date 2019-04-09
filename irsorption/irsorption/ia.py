import os
import pandas as pd
import matplotlib.pyplot as plt

import derivative
import normalization
import integration

"""
ia = interval analysis
Модуль, содержащий функции, связанные с обработкой данных на интервалах, а так
же, с их визуализацией и сохранением.
"""

"""
TODO:
Добавить выбор dpi, размера изображения, размера названия осей, размера
надписей, размера легенды.
"""

def pivot_table(data, mode=2, extrema="max"):
    """
    Формирует таблицу, информирующую о двух (начальная и конечная) или трёх
    (начальная, экстремум, конечная) точках на интервале.

    Параметры:
        data - таблица данных. Тип - pandas.DataFrame.
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

    Возвращает таблицу, с информацией о максимальной/минимальной температуре.
    Тип - pandas.DataFrame.
    """
    # Если точки две, то в таблице будут два столбца: начальная и конечная точка
    if mode == 2:
        summary = pd.DataFrame(index=["Begin", "End"])
        summary["Temperature, oC"] = [data.iloc[0], data.iloc[-1]]
        summary["Time, s"] = [data.index[0], data.index[-1]]

    # Если точки три, то в таблице будут три столбца: начальная точка, экстремум
    # и конечная точка
    if mode == 3:
        summary = pd.DataFrame(index=["Begin", "Peak", "End"])
        if extrema == "min":
            summary["Temperature, oC"] = [data.iloc[0], data.min(), data.iloc[-1]]
            summary["Time, s"] = [data.index[0], data.idxmin(), data.index[-1]]
        elif extrema == "max":
            summary["Temperature, oC"] = [data.iloc[0], data.max(), data.iloc[-1]]
            summary["Time, s"] = [data.index[0], data.idxmax(), data.index[-1]]

    return summary

def boundary_table(data, mode=2, extrema="max"):
    """
    Формирует таблицу, показывающую разность крайних точек (и экстремума, если
    точки три).

    Параметры:
        data - таблица данных. Тип - pandas.DataFrame.
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

    Возвращает таблицу с разностью значений и индексов одного (начальная и
    конечная точка) или двух (начальная, экстремум, конечная точка) интервалов.
    Тип - pandas.DataFrame.
    """
    # Если точки две, то в таблице будет один столбец: интервал
    if mode == 2:
        final = pd.DataFrame(index=["Interval"])
        final["Temperature difference, oC"] = [data.iloc[-1] - data.iloc[0]]
        final["Duration, s"] = [data.index[-1] - data.index[0]]

    # Если точки три, то в таблице будут два столбца: разность начальной точки
    # и экстремума, и разность экстремума и конечной точки.
    if mode == 3:
        final = pd.DataFrame(index=["Before", "After"])
        if extrema == "min":
            td1 = data.min() - data.iloc[0]
            td2 = data.iloc[-1] - data.min()
            final["Temperature difference, oC"] = [td1, td2]

            d1 = data.idxmin() - data.index[0]
            d2 = data.index[-1] - data.idxmin()
            final["Duration, s"] = [d1, d2]
        elif extrema == "max":
            td1 = data.max() - data.iloc[0]
            td2 = data.iloc[-1] - data.max()
            final["Temperature difference, oC"] = [td1, td2]

            d1 = data.idxmax() - data.index[0]
            d2 = data.index[-1] - data.idxmax()
            final["Duration, s"] = [d1, d2]

    return final

def integral_table(integral):
    """
    Формирует таблицу со значением интеграла и его абсолютной ошибкой.

    Параметры:
        integral - значение интеграла и абсолютной ошибки. Тип - tuple[float].

    Возвращает таблицу со значением интеграла и его абсолютной ошибкой.
    Тип - pandas.DataFrame.
    """
    table = pd.DataFrame(index=["Values"])
    table["Integral"] = integral[0]
    table["Absolute_Error"] = integral[1]
    return table

def interval_analysis(data, begin, end, keys=[], output="View", mode=2,
                      extrema="max", directory="Data/"):
    """
    Производит анализ интервала (нормировка, вычисление производной, взятие
    интеграла) и выводит информацию в файлы/Jupyter Notebook.

    Параметры:
        data - таблица данных. Тип - pandas.DataFrame.
        begin - индекс (момент времени) начала отрезка. Тип - float.
        end - индекс (момент времени) конца отрезка. Тип - float.
        keys - названия столбцов, которые нужно анализировать. Тип - list[str].
        output - режим вывода информации. Тип - str.
    Может принимать значения:
    "View" - Только визуализация.
    "Write" - Только запись значений в файл.
    "Full" - Визуализация и запись значений в файл.
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
        directory - путь к директории для записи файлов. Тип - str.
    """
    # Получение названий столбцов
    if len(keys) == 0:
        keys = data.keys()

    # Для всех столбцов
    # Выделяем данные заданного интервала
    split = data[begin:end]
    # Производим нормировку
    normalized = normalization.normalize(split, begin, end)
    # Вычисляем производные
    derivatives = derivative.derivative(normalized)
    # Вычисляем интегралы
    integrals = pd.DataFrame()
    for key in data.keys():
        integrals[key] = integration.integrate_function(normalized[key],
                                                        extrema)["Integral"]

    # Формируем путь выходного файла
    output_file = str(begin) + "-" + str(end) + "_" + "all"

    # Если режим вывода - просмотр, то отображаем блоки в Jupyter Notebook
    if output == "View":
        view_block("Все образцы:", split, "Time, s", "Temperature, $^oC$")
        view_block("Нормировка:", normalized, "Time, s", "Temperature, $^oC$")
        view_block("Производные:", derivatives, "Time, s",
                   r"dT/dt, $\frac{^oC}{s}$")
        view_block("Интегралы:", integrals, "Time, s",
                   r"$\int_{t_0}^{t} T \, dt$, $^oC \times s$")

    # Если режим вывода - запись, то записываем данные в файлы
    elif output == "Write":
        # Создаём директории для файлов
        create_directory(directory, "")
        create_directory(directory, "Data_Intervals/")
        create_directory(directory, "Data_Normalized/")
        create_directory(directory, "Data_Derivatives/")
        create_directory(directory, "Data_Integrals/")
        create_directory(directory, "Graphics_Intervals/")
        create_directory(directory, "Graphics_Normalized/")
        create_directory(directory, "Graphics_Derivatives/")
        create_directory(directory, "Graphics_Integrals/")
        create_directory(directory, "Tables_Pivot/")
        create_directory(directory, "Tables_Final/")
        create_directory(directory, "Tables_Integral/")

        # Записываем данные в файлы
        export(split, directory, "Intervals", output_file, "Time, s",
               "Temperature, $^oC$")
        export(normalized, directory, "Normalized", output_file, "Time, s",
               "Temperature, $^oC$")
        export(derivatives, directory, "Derivatives", output_file, "Time, s",
               r"dT/dt, $\frac{^oC}{s}$")
        export(integrals, directory, "Integrals", output_file, "Time, s",
               r"$\int_{t_0}^{t} T \, dt$, $^oC \times s$")

    # Если режим вывода - полный, то выводим блоки в Jupyter Notebook и
    # записываем данные в файлы
    elif output == "Full":
        # Создаём директории для файлов
        create_directory(directory, "")
        create_directory(directory, "Data_Intervals/")
        create_directory(directory, "Data_Normalized/")
        create_directory(directory, "Data_Derivatives/")
        create_directory(directory, "Data_Integrals/")
        create_directory(directory, "Graphics_Intervals/")
        create_directory(directory, "Graphics_Normalized/")
        create_directory(directory, "Graphics_Derivatives/")
        create_directory(directory, "Graphics_Integrals/")
        create_directory(directory, "Tables_Pivot/")
        create_directory(directory, "Tables_Final/")
        create_directory(directory, "Tables_Integral/")

        # Записываем данные в файлы
        export_view("Все образцы:", split, directory, "Intervals", output_file,
                    "Time, s", "Temperature, $^oC$")
        export_view("Нормировка:", normalized, directory, "Normalized",
                    output_file, "Time, s", "Temperature, $^oC$")
        export_view("Производные:", derivatives, directory, "Derivatives",
                    output_file, "Time, s", r"dT/dt, $\frac{^oC}{s}$")
        export_view("Интегралы:", integrals, directory, "Integrals",
                    output_file, "Time, s",
                    r"$\int_{t_0}^{t} T \, dt$, $^oC \times s$")

    # Для каждого столбца отдельно
    for key in keys:
        # Выделяем данные заданного интервала
        split = data[key][begin:end]
        # Производим нормировку
        normalized = normalization.normalize(data[begin:end], begin, end)[key]

        # Записываем данные о точках и интегралах в таблицы
        summary = pivot_table(split, mode, extrema)
        final = boundary_table(split, mode, extrema)
        integral = integral_table(integration.integrate(normalized, extrema))

        # Формируем путь выходного файла
        output_file = str(begin) + "-" + str(end) + "_" + key
        # Для избежания проблем с записью в файл, нужно избавиться от "/" в key
        output_file = "".join(output_file.split("/"))

        # Если режим вывода - просмотр, то отображаем таблицы в Jupyter Notebook
        if output == "View":
            print("-" * 80)
            print(key + ":")
            print(summary)
            print("\n")
            print(final)
            print("\n")
            print(integral)
            print("-" * 80)
            print("\n")

        # Если режим вывода - запись, то записываем таблицы в файлы
        elif output == "Write":
            sbody = "Tables_Pivot/" + "pivot_"
            fbody = "Tables_Final/" + "final_"
            ibody = "Tables_Integral/" + "integral_"
            summary.to_csv(directory + sbody + output_file + ".csv")
            final.to_csv(directory + fbody + output_file + ".csv")
            integral.to_csv(directory + ibody + output_file + ".csv")

        # Если режим вывода - полный, то выводим таблицы в Jupyter Notebook и
        # записываем в файлы
        elif output == "Full":
            sbody = "Tables_Pivot/" + "pivot_"
            fbody = "Tables_Final/" + "final_"
            ibody = "Tables_Integral/" + "integral_"
            summary.to_csv(directory + sbody + output_file + ".csv")
            final.to_csv(directory + fbody + output_file + ".csv")
            integral.to_csv(directory + ibody + output_file + ".csv")

            print("-" * 80)
            print(key + ":")
            print(summary)
            print("\n")
            print(final)
            print("\n")
            print(integral)
            print("-" * 80)
            print("\n")

def view_block(title, data, xlabel, ylabel):
    """
    Отображение графиков в Jupyter Notebook.

    Параметры:
        title - название графика. Тип - str.
        data - таблица с данными, которую нужно визуализировать.
    Тип - pandas.DataFrame.
        xlabel - Название оси X. Тип - str.
        ylabel - Название оси Y. Тип - str.
    """
    print("-" * 80)
    print(title)
    data.plot()
    plt.gcf().set_size_inches(20, 16)
    plt.xlabel(xlabel, fontsize=40)
    plt.ylabel(ylabel, fontsize=40)
    plt.legend(prop={'size': 30})
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.show()
    print("-" * 80)
    print("\n")

def export(data, directory, folder, output_file, xlabel, ylabel):
    """
    Запись графиков в файлы.

    Параметры:
        data - таблица с данными, которую нужно визуализировать.
    Тип - pandas.DataFrame.
        directory - путь к директории для записи файлов. Тип - str.
        folder - суффикс в названии папки, в которую будет записан файл.
    Тип - str.
        output_file - название файла, который будет сохранён. Тип - str.
        xlabel - Название оси X. Тип - str.
        ylabel - Название оси Y. Тип - str.
    """
    data.to_csv(directory + "Data_" + folder + "/data_" + output_file + ".csv")
    data.plot();
    plt.gcf().set_size_inches(20, 16)
    plt.xlabel(xlabel, fontsize=40)
    plt.ylabel(ylabel, fontsize=40)
    plt.legend(prop={'size': 30})
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.savefig(directory + "Graphics_" + folder + "/plot_" + output_file + ".png",
                dpi=80);
    plt.clf()

def export_view(title, data, directory, folder, output_file, xlabel, ylabel):
    """
    Отображение графиков в Jupyter Notebook и запись в файлы.

    Параметры:
        title - название графика. Тип - str.
        data - таблица с данными, которую нужно визуализировать.
    Тип - pandas.DataFrame.
        directory - путь к директории для записи файлов. Тип - str.
        folder - суффикс в названии папки, в которую будет записан файл.
    Тип - str.
        output_file - название файла, который будет сохранён. Тип - str.
        xlabel - Название оси X. Тип - str.
        ylabel - Название оси Y. Тип - str.
    """
    data.to_csv(directory + "Data_" + folder + "/data_" + output_file + ".csv")
    print("-" * 80)
    print(title)
    data.plot()
    plt.gcf().set_size_inches(20, 16)
    plt.xlabel(xlabel, fontsize=40)
    plt.ylabel(ylabel, fontsize=40)
    plt.legend(prop={'size': 30})
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.savefig(directory + "Graphics_" + folder + "/plot_" + output_file + ".png",
                dpi=80);
    plt.show()
    print("-" * 80)
    print("\n")

def create_directory(directory, name):
    """
    Создание директорий.

    Параметры:
        directory - путь к директории, в которой будет находиться новая
        директория. Тип - str.
        name - название новой директории. Тип - str.
    """
    try:
        os.mkdir(os.getcwd() + "/" + directory + name)
    except OSError:
        pass
