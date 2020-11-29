from . import variables
import dimod
import random
from random import randint
import neal
import numbers

ALLOW_FALSE_POSITIVE = True

def reset_default(bqm):
    variables.c_y = 100.0
    variables.c_summation = 0.75
    variables.c_xnor = -0.25
    bqm = dimod.BinaryQuadraticModel.empty(dimod.SPIN)


def get_bqm():
    bqm = dimod.BinaryQuadraticModel.empty(dimod.SPIN)
    return bqm


def get_simulated_sampler():


#    return dimod.ExactSolver()
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


def get_names(matrix, prefix):
    ans = []
    for i_row in range(len(matrix)):
        if isinstance(matrix[i_row], numbers.Number):
            ans.append(prefix + "_" + str(i_row) )
            continue
        temp = []
        for i_element in range(len(matrix[i_row])):
            temp.append(prefix + "_" + str(i_row) + str(i_element))

        ans.append(temp)
    return ans


def evaluate_affine(w, x, b):
    temp = []
    for row in w:
        suma = 0
        for i in range(len(x)):
            suma += x[i]*row[i]
        temp.append(suma)

    curr_max = None

    for i in range(len(b)):
        temp[i] += b[i]
        if i == 0:
            curr_max = temp[i]
        else:
            curr_max = max(temp[i], curr_max)
    result = []

    for element in temp:
        if element == curr_max:
            result.append(1)
        else:
            result.append(-1)
    return result


def evaluate_rnn(t, w, x, b):
    ans = []
    last = x
    for i in range(t):
        actual = evaluate_affine(w, last, b)
        ans.append(actual)
        last = actual
    return ans

def get_dec_score(annealed, real):
    score = 0.0

    for i in range(len(real)):
        for j in range(len(real[0])):
            if real[i][j] == 1:
                score += 1
            elif annealed[i][j] == -1:
                score += 1

    return score / (len(real) * len(real[0]))
def compare_answers(annealed, real):
    try:
        a = annealed[0]
        actual_score = 0
        for dec in real:
            temp = dec.outputs[1:]
            actual_score = max(actual_score, get_dec_score(annealed, temp))
        return actual_score

    except:
        annealed = annealed.outputs
        annealed = annealed[1:]
        actual_score = 0
        for dec in real:
            temp = dec.outputs[1:]
            actual_score = max(actual_score, get_dec_score(annealed, temp))
        return actual_score

    # return get_dec_score(annealed, real[0].outputs[1:])
    #real = real[1:]
    #print(real)
    #print(annealed)

    #assert (len(real) == len(annealed))
    #assert (len(real[0]) == len(annealed[0]))










