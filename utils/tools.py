from . import variables
import dimod
import random
from random import randint
import neal


def reset_default(bqm):
    variables.c_y = 100.0
    variables.c_summation = 0.75
    variables.c_xnor = -0.25
    bqm = dimod.BinaryQuadraticModel.empty(dimod.SPIN)


def get_bqm():
    bqm = dimod.BinaryQuadraticModel.empty(dimod.SPIN)
    return bqm


def get_simulated_sampler():
    return neal.SimulatedAnnealingSampler()


def get_random_identifier(length=10):
    identifier = ''.join(random.choice(variables.letters) for i in range(length))
    return identifier


def get_random_number():
    return randint(-variables.abs_numbers_range, variables.abs_numbers_range)


def get_random_matrix(n, m, is_binary=False):
    names = []
    weights = []
    temp = 0
    for i in range(n):
        names.append([])
        weights.append([])
        for j in range(m):
            names[len(names)-1].append(get_random_identifier(5))
            temp = get_random_number()
            if is_binary:
                if temp > 0:
                    temp = 1
                else:
                    temp = -1
            weights[len(weights)-1].append(temp)

    return names, weights


def get_random_dict(size):
    ans = dict()
    for i in range(size):
        ans[get_random_identifier()] = get_random_number()
    return ans


def plot_2d(labex, labely, x, y):
    pass


def get_names(matrix, prefix):
    ans = []
    for i_row in len(matrix):
        temp = []
        for i_element in len(matrix[i_row]):
            temp.append(prefix + "_" + str(i_row) + str(i_element))

        ans.append(temp)
    return ans
