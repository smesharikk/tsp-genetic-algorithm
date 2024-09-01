import random
import math
from itertools import cycle  # модуль для создания бесконечных итераторов
import matplotlib.pyplot as plt

t = """0.00 12.53 5.10 11.70 3.00 13.04 4.47 1.00 8.49 7.62 10.00 13.15 13.00 13.60 13.15 
12.53 0.00 10.05 10.00 11.40 7.28 13.45 13.04 13.00 8.06 5.39 8.25 6.32 2.83 4.47 
5.10 10.05 0.00 13.45 2.24 13.42 9.06 6.08 12.08 2.83 5.83 13.89 13.00 12.04 12.37 
11.70 10.00 13.45 0.00 13.04 3.61 9.00 11.40 5.39 13.60 13.00 2.83 4.47 8.25 6.32 
3.00 11.40 2.24 13.04 0.00 13.60 7.28 4.00 10.82 5.00 7.81 13.93 13.34 13.04 13.04 
13.04 7.28 13.42 3.61 13.60 0.00 11.40 13.00 8.60 12.81 11.40 1.00 1.00 5.00 3.00 
4.47 13.45 9.06 9.00 7.28 11.40 0.00 3.61 4.47 11.05 12.65 11.18 11.70 13.60 12.53 
1.00 13.04 6.08 11.40 4.00 13.00 3.61 0.00 7.81 8.54 10.82 13.04 13.04 13.93 13.34 
8.49 13.00 12.08 5.39 10.82 8.60 4.47 7.81 0.00 13.34 14.00 8.06 9.22 12.21 10.63 
7.62 8.06 2.83 13.60 5.00 12.81 11.05 8.54 13.34 0.00 3.16 13.45 12.21 10.44 11.18 
10.00 5.39 5.83 13.00 7.81 11.40 12.65 10.82 14.00 3.16 0.00 12.21 10.63 8.06 9.22 
13.15 8.25 13.89 2.83 13.93 1.00 11.18 13.04 8.06 13.45 12.21 0.00 2.00 6.00 4.00 
13.00 6.32 13.00 4.47 13.34 1.00 11.70 13.04 9.22 12.21 10.63 2.00 0.00 4.00 2.00 
13.60 2.83 12.04 8.25 13.04 5.00 13.60 13.93 12.21 10.44 8.06 6.00 4.00 0.00 2.00 
13.15 4.47 12.3 7 6.32 13.04 3.00 12.53 13.34 10.63 11.18 9.22 4.00 2.00 2.00 0.00"""

cities = []  # двумерная матрица расстояний между городами
for row in t.split("\n"):
    nums = [float(i) for i in row.strip().split(" ")]
    cities.append(nums)


def toch_mut(travel):
    """
    Точечная мутация
    :param travel: Путь
    :return: Измененный путь
    Функция осуществляет мутацию путем обмена местами двух соседних городов в маршруте.
    """
    a = random.randint(0, len(travel) - 2)
    m = travel[a]
    travel[a] = travel[a + 1]
    travel[a + 1] = m
    return travel


def salt_mut(travel):
    """
    для мутации сальтацией
    :param travel: Путь
    :return: Измененный путь
    """
    a = 0
    b = 0
    while a == b:
        a = random.randint(0, len(travel) - 1)
        b = random.randint(0, len(travel) - 1)
    m = travel[a]
    travel[a] = travel[b]
    travel[b] = m
    return travel


def order_crossover(parent1, parent2):
    """
    Секция кроссовера копируется
полностью из 1го родителя. Остальные аллели копируются из
2го родителя, начиная со 2й точки разрыва.

    для порядкового кроссовера
    Кроссовер OX
    :param parent1: Родитель 1
    :param parent2: Родитель 2
    :return: [Ребенок 1, Ребенок 2]
    """
    lenpar = len(parent1)
    a = math.floor(lenpar / 3.0)
    b = math.ceil(lenpar / 3.0) + a

    child1 = parent1[a:b]
    cycleparent2 = cycle(parent2)
    for i in range(b):
        next(cycleparent2)
    i = 0
    while i < (len(parent1) - b):
        t = next(cycleparent2)
        if not (t in child1):
            child1.append(t)
            i += 1
    i = 0
    while i < (a):
        t = next(cycleparent2)
        if not (t in child1):
            child1.insert(i, t)
            i += 1

    child2 = parent2[a:b]
    cycleparent1 = cycle(parent1)
    for i in range(b):
        next(cycleparent1)
    i = 0
    while i < (len(parent1) - b):
        t = next(cycleparent1)
        if not (t in child2):
            child2.append(t)
            i += 1
    i = 0
    while i < (a):
        t = next(cycleparent1)
        if not (t in child2):
            child2.insert(i, t)
            i += 1

    return [child1, child2]


def partial_mapped_crossover(parent1, parent2):
    """
     для кроссовера с частичным отображением
    Кроссовер PMX
    :param parent1: Родитель 1
    :param parent2: Родитель 2
    :return: [Ребенок 1, Ребенок 2]
    """

    lenpar = len(parent1)
    a = math.floor(lenpar / 3.0)
    b = math.ceil(lenpar / 3.0) + a

    child1 = parent1[a:b]
    t = parent2.copy()
    for i in range(len(t)):
        aa = t[i]
        while t[i] in parent1[a:b]:
            if (aa == parent2[parent1.index(t[i])]):
                break
            t[i] = parent2[parent1.index(t[i])]
    cycleparent2 = cycle(t)
    for i in range(b):
        next(cycleparent2)
    i = 0
    while i < (len(parent1) - b):
        t = next(cycleparent2)
        if not (t in child1):
            child1.append(t)
            i += 1
    i = 0
    while i < (a):
        t = next(cycleparent2)
        if not (t in child1):
            child1.insert(i, t)
            i += 1

    child2 = parent2[a:b]
    t = parent1.copy()
    for i in range(len(t)):
        aa = t[i]
        while t[i] in parent2[a:b]:
            if (aa == parent1[parent2.index(t[i])]):
                break
            t[i] = parent1[parent2.index(t[i])]
    cycleparent1 = cycle(t)
    for i in range(b):
        next(cycleparent1)
    i = 0
    while i < (len(parent1) - b):
        t = next(cycleparent1)
        if not (t in child2):
            child2.append(t)
            i += 1
    i = 0
    while i < (a):
        t = next(cycleparent1)
        if not (t in child2):
            child2.insert(i, t)
            i += 1
    return [child1, child2]
    # return (child1, child2)


def rulet_parent(cities=cities):
    """
    9лаба
    Создание начальной популяции, жадный алгоритм с внедрением случайного механизма
    :param cities: Массив городов
    :return: Путь
    """
    notincledet = [i for i in range(len(cities[0]))]
    travel = [random.choice(notincledet)]
    notincledet.remove(travel[0])
    i = 0
    dist = 0
    while len(notincledet) > 0:
        i += 1
        t = [random.choices(notincledet, weights=[1/float(cities[travel[-1]][i]) for i in notincledet],
                            k=len(notincledet))[-1]]
        dist += float(cities[travel[-1]][t[0]])
        travel.append(t[0])
        notincledet.remove(t[0])
    return (travel)


def rand_parent(cities=cities):
    """
    Создание начальной популяции, случайно с контролем популяции 1шт
    :param cities: Массив городов
    :return: Путь
    """
    notincledet = [i for i in range(len(cities[0]))]
    travel = [random.choice(notincledet)]
    notincledet.remove(travel[0])
    i = 0
    dist = 0
    while len(notincledet) > 0:
        i += 1
        t = [random.choice(notincledet)]
        dist += float(cities[travel[-1]][t[0]])
        travel.append(t[0])
        notincledet.remove(t[0])
    return (travel)


def get_dist(travel, cities=cities):
    """
    Дистанция пути
    :param travel: Путь
    :param cities:
    :return: Дистанция
    """
    dist = 0
    for i in range(len(travel) - 1):
        dist += float(cities[travel[i]][travel[i + 1]])
    return (dist)


def get_distarr(population):
    """
    Минимальная дистанция популяции
    :param population: Популяция
    :return: Мин дист
    """
    a = []
    for i in range(len(population) - 1):
        a.append(get_dist(population[i]))
    return (min(a))


def bin_tour(population):
    """
    Бинарный бета-турнир
    :param population: Популяция
    :return: Популяция
    """
    pop2 = []
    for i in range(len(population)):
        a = random.choices(population, k=2)
        pop2.append(min(a, key=lambda x: get_dist(x)))
    return (pop2)


def lin_rang(population, nMinus=0, nPlus=2):
    """
    Линейная ранговая селекция
    :param population: Популяция
    :param k:
    :param nMinus:
    :param nPlus:
    :return: Популяция
    """
    population.sort(key=lambda x: get_dist(x) * (-1))
    manychild = []
    for i in range(len(population)):
        manychild.append(random.choices(population, weights=[
            (nMinus + (nPlus - nMinus) * ((population.index(i)) / (len(population) - 1))) / len(population) for i in
            population], k=1)[0])

    return manychild


def rand_population(population):
    a = random.randint(0, len(population) - 1)
    return (population[a])


# print("Выберите оператор для создания начальной популяции \n "
#       "1)Случайный с контролем ограничений \n"
#       " 2)Жадный алгоритм с внедрением случайного механизма")
# genpopulation = [rand_parent, rulet_parent][int(input()) - 1]
# print("Выберите оператор кроссовера \n "
#       "1)Порядковый OX\n"
#       " 2)Частичного отображения PMX")
# crospopulation = [order_crossover, partial_mapped_crossover][int(input()) - 1]
# print("Выберите оператор мутации \n "
#       "1)Точечная мутация\n"
#       " 2)Сальтация")
# mutpopulation = [toch_mut, salt_mut][int(input()) - 1]
# print("Выберите оператор селекции \n "
#       "1)Линейная ранговая схема селекции\n"
#       " 2)Бинарный бета-турнир")
# selpopulation = [lin_rang, bin_tour][int(input()) - 1]


# Генерация случайных путей для начальной популяции
def nach_test(arrcount, cities=cities):
    # Генерация случайных путей для начальной популяции
    poptest = [rand_parent() for i in range(arrcount * 2)]
    return poptest


arrcount = 5
poptest = nach_test(arrcount)

# Функция для тестирования алгоритма оптимизации


def test(poptest, selpopulation, arrcount, crospopulation, mutpopulation):
    arrcount = arrcount
    population = poptest
    populationarr = []
    distarr = []
    populationarr.append(population)
    distarr.append(get_distarr(population))

    for i in range(30):
        # print(population,"1")
        # Создание новой популяции на основе текущей
        population = []
        for j in range(int(len(populationarr[-1]) / 2)):
            population += crospopulation(rand_population(
                populationarr[-1]), rand_population(populationarr[-1]))
        # print(population,"2")
        # Мутация новой популяции
        for j in range(len(population)):
            population[j] = mutpopulation(population[j])
        # print(population,"3")1
        # Применение оператора селекции к новой популяции
        population = selpopulation(population)
        # Добавление лучшего индивида из предыдущего поколения в новую популяцию
        population.append(min(populationarr[-1], key=lambda x: get_dist(x)))
        populationarr.append(population)
        # Вычисление дистанции лучшего индивида в текущем поколении и добавление в список дистанций
        distarr.append(
            get_dist(min(populationarr[-1], key=lambda x: get_dist(x))))
        # print(populationarr, distarr)
        i += 1
        # print(f"Номер поколения {i}, Лучшая особь {population[-1]}, Дистанция {get_dist(population[-1])}")
    return (population, get_dist(population[-1]), distarr)


# выполняет серию экспериментов для оценки двух различных операторов
# мутации: toch_mut и salt_mut. Для каждого из этих операторов мутации
# производится 10 запусков функции test
crospopulation = order_crossover
mutpopulation = toch_mut
selpopulation = bin_tour
tt = []  # Список для хранения результатов экспериментов
coltest = 10
for i in range(coltest):
    t = test(poptest, selpopulation, arrcount, crospopulation, mutpopulation)
    tt.append(t)
# Вычисление средней дистанции для toch_mut
avegdist1 = sum([i[1] for i in tt]) / len(tt)

mutpopulation = salt_mut
tt = []
for i in range(coltest):
    t = test(poptest, selpopulation, arrcount, crospopulation, mutpopulation)
    tt.append(t)
# Вычисление средней дистанции для salt_mu
avegdist2 = sum([i[1] for i in tt]) / len(tt)
print(f"Точечная мутация {avegdist1}")
print(f"Сальтация {avegdist2}")

plt.bar([1, 2], [avegdist1, avegdist2])
plt.show()
