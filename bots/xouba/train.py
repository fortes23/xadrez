import os
import sys
import random
import json
import argparse

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../../xadrez')

from pool import Pool  # noqa: E402

length = 8*8


def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--json', help='Start from previous json',
                        action='store', required=True)
    args = parser.parse_args()
    return args


def individual(min, max):
    ind = {"p": {"wpos": [random.randint(min, max) for i in range(length)],
                 "wmat": random.randint(min, max)},
           "n": {"wpos": [random.randint(min, max) for i in range(length)],
                 "wmat": random.randint(min, max)},
           "b": {"wpos": [random.randint(min, max) for i in range(length)],
                 "wmat": random.randint(min, max)},
           "r": {"wpos": [random.randint(min, max) for i in range(length)],
                 "wmat": random.randint(min, max)},
           "q": {"wpos": [random.randint(min, max) for i in range(length)],
                 "wmat": random.randint(min, max)},
           "k": {"wpos": [random.randint(min, max) for i in range(length)],
                 "wmat": random.randint(min, max)}}
    return ind


def generate_population(num_individuals):
    return [individual(-100, 100) for i in range(num_individuals)]


def calc_fitness(individual):
    fitness = 0

    json_file = os.path.dirname(os.path.realpath(__file__)) + '/test.json'
    with open(json_file, 'w') as fp:
        json.dump(individual, fp, ensure_ascii=False)

    bot1 = os.path.dirname(os.path.realpath(__file__)) + '/xouba.py'
    bot2 = os.path.dirname(os.path.realpath(__file__)) + '/../stockfishbot.py'
    # bot3 = os.path.dirname(os.path.realpath(__file__)) + '/../randombot.py'

    p1 = Pool(bot1=[bot1, '-j', json_file], bot2=[bot2], debug=True)
    p2 = Pool(bot1=[bot1, '-j', json_file], bot2=[bot2, '-l', '2'], debug=True)
    # p2 = Pool(bot1=[bot1, '-j', json_file], bot2=bot2, debug=True)
    # p3 = Pool(bot1=[bot1, '-j', json_file], bot2=bot3, debug=True)

    matches = [p1, p2]

    for p in matches:
        for _ in range(15):
            p.match()
            if p.last_result == p.RESULT_WIN_WHITE:
                fitness += 5
            elif p.last_result == p.RESULT_DRAW:
                fitness += 1
            p.reset_chess_board()
        del p

    return fitness


def selection_and_crossover(population, pressure):
    points = [(calc_fitness(i), i) for i in population]

    # Sort fitness and save only the individuals data
    points = [i[1] for i in sorted(points, key=lambda x: x[0])]
    population = points

    # Get last individuals
    selected = points[(len(points) - pressure):]

    # Mix genetical material
    for i in range(len(selected)):
        for p in population[0]:
            _entrypoint = random.randint(0, length - 1)
            parents = random.sample(selected, 3)

            population[i][p]['wpos'][:_entrypoint] = parents[0][p]['wpos'][:_entrypoint]
            population[i][p]['wpos'][_entrypoint:] = parents[1][p]['wpos'][_entrypoint:]
            population[i][p]['wmat'] = parents[2][p]['wmat']

    return population


def mutation(population, pressure, mutation_chance=0.2):
    # mutation_chance robability that an individual mutates
    for i in range(len(population) - pressure):
        # All individuals, except parents, can mute.
        if random.random() <= mutation_chance:
            for p in population[0]:
                # npoints are selected
                npoints = random.randint(1, length)
                new_wpos = [random.randint(-100, 100) for i in range(npoints)]

                while new_wpos == population[i][p]['wpos'][npoints:]:
                    new_wpos = [random.randint(-100, 100) for i in range(npoints)]

                population[i][p]['wpos'][-npoints:] = new_wpos

                if random.random() <= mutation_chance:
                    new_wmat = random.randint(0, 1000)
                    population[i][p]['wmat'] = new_wmat

    return population


pressure = 15

args = parser_args()
with open(args.json, "r") as f:
    jsf = json.load(f)
    population = jsf

population += generate_population(50-len(population))

for it_round in range(400):
    print("*****" + str(it_round) + "*****")
    population = selection_and_crossover(population, pressure)
    population = mutation(population, pressure)

    result_train = os.path.dirname(os.path.realpath(__file__)) + '/result_train.json'
    with open(result_train, 'w') as fp:
        json.dump(population, fp, ensure_ascii=False)
