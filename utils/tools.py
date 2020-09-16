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


def get_random_dict(size):
    ans = dict()
    for i in range(size):
        ans[get_random_identifier()] = randint(-variables.abs_numbers_range, variables.abs_numbers_range)
    return ans

def plot_2d(labex, labely, x, y):
    pass
