import random
import threading

import numpy
import sys

import time

from deap import base
from deap import creator
from deap import tools
from deap import algorithms
from deap import gp
from itertools import tee, islice, chain, izip
from route import Individual
from fix_route import FixRoute

edges = 0
edgesList = list()
tempList = list()
tmpEdges = list()

# sys.setrecursionlimit(1000000)

def current_and_next(list):
    a, b = tee(list)
    next(b, None)
    return izip(a, b)

def eval(individual):
    val = 0;
    for current,nxt in current_and_next(individual[0].values):
        val = val + findValue(current,nxt)
    return (val,)

def readData(name,lst):
    with open(name) as fl:
        edges = fl.readline()
        for ln in fl:
            lst.append(map(int,ln.rstrip().split(" ")))

def findValue(a,b):
    for edge in edgesList:
        if edge[0] == a and edge[1] == b:
            return edge[2]
        if edge[1] == a and edge[0] == b:
                return edge[3]
    exit()
    return 0

def generateIndividual():
    individual = Individual(edgesList)
    individual.getRoute()

    return individual


def mate(ind1, ind2):
    fix_route = FixRoute(edgesList)
    parts1 = numpy.array_split(ind1[0].values, 3)
    parts2 = numpy.array_split(ind2[0].values, 3)
    new_values1 = []
    new_values2 = []

    new_values1.extend(parts1[0])
    new_values1.extend(parts2[1])
    new_values1.extend(parts1[2])

    new_values2.extend(parts2[0])
    new_values2.extend(parts1[1])
    new_values2.extend(parts2[2])

    # ind1[0].values = fix_route.getFixedRoute(new_values1)
    # ind2[0].values = fix_route.getFixedRoute(new_values2)

    route1 = fix_route.repair(new_values1)
    route2 = fix_route.repair(new_values2)

    ind1[0].values = route1
    ind2[0].values = route2

    # route = [1, 6, 5, 4, 7, 1, 8, 3, 2, 4, 5, 1, 1, 1,5,6,1,2,5,4,7,8,2,5,6, 2, 6, 5, 6, 2, 1, 5, 1]
    # print(route1, route2)

    return ind1, ind2


def mutate(ind1):
    mutate = random.randrange(1, len(ind1[0].values) - 2)
    common_peak = findCommonPeak(ind1[0].values[mutate-1],ind1[0].values[mutate+1])

    # print(ind1[0].values)
    # print(mutate, common_peak)
    if common_peak is not False:
        ind1[0].values[mutate] = findCommonPeak(ind1[0].values[mutate-1],ind1[0].values[mutate+1])

    # print(ind1[0].fitness.values)

    return [ind1]


def findCommonPeak(peak1, peak2):
    peak1_found = []
    peak2_found = []

    for edge in edgesList:
        if edge[0] == peak1:
            peak1_found.append(edge[1])

        if edge[1] == peak1:
            peak1_found.append(edge[0])

        if edge[0] == peak2:
             peak2_found.append(edge[1])

        if edge[1] == peak2:
            peak2_found.append(edge[0])

    common = list(set(peak1_found).intersection(peak2_found))

    if len(common) == 0:
        return False # jesli nie ma wspolnych to zwroc false
    else:
        return random.choice(common) # zwroc losowy

def main():
    readData("50_dane.txt", edgesList)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initRepeat, creator.Individual, generateIndividual,1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", eval)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register('mutate', mutate)
    toolbox.register('mate', mate)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Min", min)
    stats.register("Max", max)

    pop = toolbox.population(n=100)

    NGEN = 100
    start = time.time()

    for gen in range(NGEN):
        offspring = algorithms.varAnd(pop, toolbox, cxpb=0.1, mutpb=0.1)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        pop = toolbox.select(offspring, k=len(pop))
        top3 = tools.selBest(pop, k=1)
        for best in top3:
            print "generation:",gen," fitness best:",best.fitness," population statistics:",stats.compile(pop)

    end = time.time()
    print end - start, "s"

if __name__ == '__main__':
    sys.setrecursionlimit(1000000000)
    threading.stack_size(200000000)
    thread = threading.Thread(target=main)
    thread.start()
    # main()