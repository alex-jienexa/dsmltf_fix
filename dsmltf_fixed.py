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

def mean_vector(sample: list[N]) -> list[N]:
    """
    Возвращает вектор отклонений от среднего
    """
    return [x_i - mean(sample) for x_i in sample]

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
    return sum(math.pow(x - mean(sample), 2) for x in sample) / len(sample)-1

def pvariance(sample: list[N]) -> float:
    """
    Считает дисперсию населения выборки.
    Используется тогда, когда у ваша выборка - это вся некоторая совокупность данных.
    """
    return sum(math.pow(x - mean(sample), 2) for x in sample) / len(sample)

def std_deviation(sample: list[N]) -> float:
    """
    Считает стандартное отклонение выборки.
    Стандартное отклонение считает, как сильно отклоняются данные от среднего арифметического выборки.
    То есть если значение отклонения равно 2, то данные отклоняются в среднем на 2 значения
    """
    # стандартное отклонение равно корню дисперсии
    return math.sqrt(variance(sample))

def interquantile_range(sample:list[N]) -> float:
    """
    Рассчитывает интерквантильный размах в выборке. Оно равно разности между 0.25-квантилями и 0.75-квантилями
    """
    return quantile(sample, 0.75) - quantile(sample, 0.25)

def inrange_items(sample: list[N]) -> list[N]:
    """
    Возвращает список элементов, находящихся в пределах диапазона [Q1 - i_r; Q3 + i_r], где Q1, Q3 равны quantile(sample, 0.25) и quantile(sample, 0.75)
    соответственно, а i_r равен interquantile_range(sample) 
    """
    _ss = sorted(sample)
    _left = quantile(sample, 0.25) - (interquantile_range(sample) * 1.5)
    _right = quantile(sample, 0.75) + (interquantile_range(sample) * 1.5)
    return [item for item in _ss if _left <= item <= _right]

def minor_items(sample: list[N]) -> list[N]:
    """
    Возвращает список элементов, имеющих незначительное отклонение. Такие элементы находятся
    вне диапазона ``[Q1 - i_r*1.5; Q3 + i_r*1.5]``, где Q1, Q3 равны quantile(sample, 0.25) и quantile(sample, 0.75)
    соответственно, а i_r равен interquantile_range(sample) 
    """
    _ss = sorted(sample)
    _left = quantile(sample, 0.25) - (interquantile_range(sample) * 1.5)
    _right = quantile(sample, 0.75) + (interquantile_range(sample) * 1.5)
    return [item for item in _ss if not(_left <= item <= _right)]

def major_items(sample: list[N]) -> list[N]:
    """
    Возвращает список элементов, имеющих значительное отклонение. Такие элементы находятся вне
    диапазонеа ``[Q1 - i_r*3; Q3 + i_r*3]``, где Q1, Q3 равны quantile(sample, 0.25) и quantile(sample, 0.75)
    соответственно, а i_r равен interquantile_range(sample) 
    """
    _ss = sorted(sample)
    _left = quantile(sample, 0.25) - (interquantile_range(sample) * 3)
    _right = quantile(sample, 0.75) + (interquantile_range(sample) * 3)
    return [item for item in _ss if not(_left <= item <= _right)]

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
    
def f_norm(x: N, mu: float=0, sigma: float=1):
    """
    Функция распределения стандартного нормального отклонения через функцию ошибок (erf)
    Check: https://ru.wikipedia.org/wiki/%D0%9D%D0%BE%D1%80%D0%BC%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5_%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5#%D0%A4%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D1%8F_%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F
    
    Вообще предполагается что mu равно среднему (mean), а signa - стандартному отклонению
    """
    return (1 + math.erf((x-mu)/(sigma*math.sqrt(2))))/2

def inv_f_norm(p, mu, s, t=0.001):
    """
    Функция обратного нормального распределения.
    """
    # сначала перейдем к стандартному нормальному распределению
    if mu != 0 or s != 1:
        return mu + s * inv_f_norm(p, 0, 1, t)
    # ищем в полосе значений -100…100
    low_x = -100.0
    low_p = 0
    hi_x = 100.0    # эти переменные не используются
    hi_p = 1        #
    while hi_x - low_x > t:
        mid_x = (low_x + hi_x)/2
        mid_p = f_norm(mid_x) # or (low_p + hi_p)/2?
        if mid_p < p:
            low_x = mid_x
            low_p = mid_p
        elif mid_p > p:
            hi_x = mid_x
            hi_p = mid_p
        else:
            break
    return mid_x
