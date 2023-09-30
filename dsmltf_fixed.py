"""
----------------------------------------------------------------
Исправленная версия dsmltf.py, созданная для предмета Интеллектуальный анализ данных

Код создан https://github.com/alex-jienexa для кфу-страдальцев
Файл будет пополняться по мере появления практических работ по предмету

Кроме того, читая этот код можно хоть что-то полезное узнать

----------------------------------------------------------------
ИМПОРТ:
Кидаете этот файл в папку с вашим кодом, и..
    import dsmltf_fixed as dataanal
...ну или другим известным вам импортом
----------------------------------------------------------------
"""
from typing import TypeVar
from collections import Counter
import math

T = TypeVar('T')
"""Любой тип данных"""
N = TypeVar('N', int, float)    
""" Числовые типы данных - int и float """


def scope(sample: list[N]) -> N:
    """
    Считает Размах выборки - разницу между максимальным или минимальным значением выборки.

    --- Parameters --- \n
    sample: list - необходимая выборка

    --- Returns --- \n
    float - размах данной выборки
    """
    return max(sample) - min(sample)

def mean(sample: list[N]) -> float:
    """
    Среднее арифметическое чисел
    """
    return sum(sample) / len(sample)

def meanOf2(sample_x: list[N], sample_y: list[N]) -> float:
    """
    Считает выборочные средние двух выборок, то есть mean(a*b)
    """
    if len(sample_x) != len(sample_y):
        raise ValueError(f"Длины выборок sample_x и sample_y должны быть равны, а не: {len(sample_x)} and {len(sample_y)}")
    return sum([sample_x[i] * sample_y[i] for i, _ in enumerate(sample_x)]) / len(sample_x)

def mode(sample: list[T]) -> T:
    """
    Самый частовстречающийся элемент в выборке
    Это называется модой выборки. Встретил на одном сайте название "режим образца", который тоже относится к выборке...
    """
    c = Counter(sample)     # словарь по типу (xK, y), где xK - некоторый 
                            # элемент выборки, а y - число вхождений xK в выборку
    return c.most_common(1)[0][0]   # most.common(1) возвращает list[Tuple[...]] самых частовстречающихся значений
                                    # тут нужно просто взять популярную переменную

def mode_list(sample: list[T], items: int = 1) -> list[T]:
    """
    Возвращает список из items самых частовстрещающихся значений в выборке.
    """
    if (items <= 0):
        raise ValueError(f"Элемент items должен быть больше 0, не {items}")
    c = Counter(sample)
    return [k[0] for k in c.most_common(items)]

def median(sample: list[N]) -> float:
    """
    Поиск медианы выборки. Медианой называют число, которое является некоторой мерединой выборки, т.е. средним значением в выборке.
    """
    # Медиана находится упорядочиванием выборки, то есть его сортировкой
    n = len(sample)
    index = n // 2
    if index % 2 == 0:  
        # выборка с чётным объемом - возврат среднего арифметического двух элементов близких к медиане
        return sum(sorted(sample)[index-1:index+1]) / 2
    else:
        # Выборка с нечётным объемом - возврат элемента посередине отсортированной выборки
        return sorted(sample)[index]

def frequency(sample: list[T], item: T) -> int:
    """
    Возврат частоты встречи элемента item в выборке.
    """
    c = Counter(sample)
    return c.get(item)

def rel_frequency(sample: list[T], item: T) -> float:
    """
    Возвращает относительную частоту item в выборке в пределах [0, 1]. Если вы хотите вернуть в процентах, умножьте результат
    на 100 или воспользуйтесь relp_frequency(...)
    Относительная частота - это отношение частоты к общему числу данных.
    """
    return frequency(sample, item)/len(sample)

def relp_frequency(sample: list[T], item: T) -> float:
    """
    Возвращает относительную частоту item в выборке в процентах.
    Относительная частота - это отношение частоты к общему числу данных.
    """
    return rel_frequency(sample, item) * 100

def quantile(sample: list[N], part: float) -> float:
    """
    Возвращает значение, меньше которого part*100% предметов в выборке - квантиль выборки.
    Медиана матрицы является частным случаем квантиля (0.5)
    """
    part = part * len(sample)
    if part == int(part): # получился целый результат
        return sorted(sample)[int(part)]
    else:
        part = round(part)
        return sum(sorted(sample)[part-1:part+1]) / 2

def quantile_item(sample: list[T], part: float) -> T:
    """
        Возвращает элемент, который претендует на место квантиля. Если таких элементов два (между ними),
        то возвращает ближайший к нему по типу округления.
        Т.е. получился элемент 3,25 -> возврат [3]
        получился элемент 3,75 -> возврат 4

        See also: quantile(...)
    """
    part = part * len(sample)
    return sorted(sample)[round(part)]

def variance(sample: list[N]) -> float:
    """
    Считает дисперсию выборки.
    Дисперсия - основной показатель статистики, показывающий разброс элементов в выборке. 
    Отвечает за разнородность результата и вероятность встретить "не среднее" значение в выборке - чем оно выше, тем больше вероятность.
    """
    return sum([math.pow(x - mean(sample), 2) for x in sample])/len(sample)

def std_deviation(sample: list[N]) -> float:
    """
    Считает стандартное отклонение выборки.
    Стандартное отклонение считает, как сильно отклоняются данные от среднего арифметического выборки.
    То есть если значение отклонения равно 2, то данные отклоняются в среднем на 2 значения
    """
    # стандартное отклонение равно корню дисперсии
    return math.sqrt(variance(sample))

def interquartile_range(sample:list[N]) -> float:
    """
    Рассчитывает интерквартильный размах в выборке. Оно равно разности между 0.25-квантилями и 0.75-квантилями
    """
    return quantile(sample, 0.75) - quantile(sample, 0.25)

def covariation(sample_x: list[N], sample_y: list[N]) -> float:
    """
    Возвращает ковариацию двух выборок - попытка определить изменение двух выборок в том же направлении.
    Является отклонением переменных от своих средих.
    """
    return meanOf2(sample_x, sample_y) - mean(sample_x) * mean(sample_y)

def correlation(sample_x: list[N], sample_y: list[N]) -> float:
    """
    Считает корреляцию двух выборок - показатель тесноты связи между ними. Такой показатель имеет значения от -1 до 1 и
    показывает связи между признаками. Анализировать связь можно по шкале Чеддока:
    * 0.1 < rxy < 0.3: слабая;
    * 0.3 < rxy < 0.5: умеренная;
    * 0.5 < rxy < 0.7: заметная;
    * 0.7 < rxy < 0.9: высокая;
    * 0.9 < rxy < 1: весьма высокая;

    Также определяется тип связи, прямая (если > 0) и обратная (если <= 0)
    """
    return covariation(sample_x, sample_y) / (std_deviation(sample_x) * std_deviation(sample_y))

def regression_coef(main_list: list[N], sec_list: list[N]) -> float:
    """
    Считает коэфициент регрессии первого списка на другой.
    Смысл такого коэфициента объясняется в следующем: если увеличить значение `sec_list` на 1, то
    значение `main_list` изменится на `regression_coef()`.
    """
    return covariation(main_list, sec_list) / (std_deviation(sec_list) ** 2)
