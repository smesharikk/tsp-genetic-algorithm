import random
import math
from itertools import cycle  # модуль для создания бесконечных итераторов
from itertools import product

t = """0.00 12.53 5.10 11.70 3.00
12.53 0.00 10.05 10.00 11.40
5.10 10.05 0.00 13.45 2.24
11.70 10.00 13.45 0.00 13.04
3.00 11.40 2.24 13.04 0.00"""
answer = 36.989999999999995
minim_pogresh = 100 ** 100
dist_ans = 0

# Преобразование: удаление лишних пробелов
cleaned_t = "\n".join(" ".join(row.split()) for row in t.splitlines())

# Преобразование строки cleaned_t в матрицу расстояний
cities = []
for row in cleaned_t.split("\n"):
    nums = [float(i) for i in row.strip().split(" ")]
    cities.append(nums)


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


def get_dist(travel, cities=cities):
    """
    Дистанция пути с возвратом в исходную точку
    :param travel: Путь
    :param cities: Матрица расстояний между городами
    :return: Дистанция
    """
    dist = 0
    for i in range(len(travel) - 1):
        dist += float(cities[travel[i]][travel[i + 1]])

    # Добавляем расстояние от последнего города к первому
    dist += float(cities[travel[-1]][travel[0]])

    return dist


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


def rand_population(population):
    a = random.randint(0, len(population) - 1)
    return (population[a])


# Словарь с функциями
functions = {
    "rand_parent": rand_parent,
    "rulet_parent": rulet_parent,
    "order_crossover": order_crossover,
    "partial_mapped_crossover": partial_mapped_crossover,
    "toch_mut": toch_mut,
    "salt_mut": salt_mut,
    "lin_rang": lin_rang,
    "bin_tour": bin_tour
}

# Матрица с именами функций
matrix = [["rand_parent", "rulet_parent"],
          ["order_crossover", "partial_mapped_crossover"],
          ["toch_mut", "salt_mut"],
          ["lin_rang", "bin_tour"]]

# Генерация всех возможных комбинаций
combinations = list(product(*matrix))

# Перебор всех комбинаций и выполнение соответствующих функций
for combination in combinations:
    result = ""
    print(", ".join(combination))
    genpopulation = functions[combination[0]]
    crospopulation = functions[combination[1]]
    mutpopulation = functions[combination[2]]
    selpopulation = functions[combination[3]]

    arrcount = 5
    population = [genpopulation() for _ in range(arrcount * 2)]
    populationarr = []
    distarr = []
    populationarr.append(population)
    distarr.append(min(get_dist(p, cities) for p in population))
    flag = True
    i = 0
    while flag:
        population = []
        for _ in range(int(len(populationarr[-1]) / 2)):
            population += crospopulation(random.choice(
                populationarr[-1]), random.choice(populationarr[-1]))
        for j in range(len(population)):
            population[j] = mutpopulation(population[j])
        population = selpopulation(population)
        population.append(min(populationarr[-1], key=lambda x: get_dist(x)))
        populationarr.append(population)
        distarr.append(
            get_dist(min(populationarr[-1], key=lambda x: get_dist(x))))
        i += 1
        if len(distarr) > 100 and len(set(distarr[-40:])) == 1:
            flag = False
        result = "Номер поколения: " + str(i) + " Лучшая особь: " + str(
            population[-1]) + " Дистанция: " + str(get_dist(population[-1]))

    print(result)
    pogresh = ((get_dist(population[-1]) - answer) / answer) * 100
    distantion = get_dist(population[-1])
    print(
        f"погрешность: {pogresh}% ")
    if pogresh < minim_pogresh:
        minim_pogresh = pogresh
        copied_tuple = combination[:]
        dist_ans = distantion
    print("==================================")

print(
    f"Лучше всего использовать операторы: { ', '.join(copied_tuple)}, дистанция: {dist_ans}, погрешность {minim_pogresh}")
