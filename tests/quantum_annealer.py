from quantum_sampler.quantum_sampler import Quantum_Sampler
from utils.tools import get_random_matrix, compare_answers, evaluate_rnn


def test1():
    '''
    using simple connection between timesteps
    :return:
    '''
    score = 0
    iterations = 5
    subtests = 10
    for m in range(2, iterations+1):
        for i in range(subtests):
            w = get_random_matrix(m, m)
            w = w[1]

            x = get_random_matrix(1, m, True)
            x = x[1][0]

            b = get_random_matrix(1, m, False)
            b = b[1][0]
            rnn_sampler = Quantum_Sampler(2, w, x, b, workflow="simulated")
            annealed = rnn_sampler.execute()
            print(annealed)
            score += compare_answers(annealed, 2, w, x, b)

    print(score/((iterations - 1)*subtests))


def test2():
    '''
    using simple connection between timesteps
    :return:
    '''
    score = 0
    iterations = 5
    subtests = 10
    for m in range(2, iterations+1):
        for i in range(subtests):
            w = get_random_matrix(m, m)
            w = w[1]

            x = get_random_matrix(1, m, True)
            x = x[1][0]

            b = get_random_matrix(1, m, False)
            b = b[1][0]

            print(w, x, b)

            rnn_sampler = Quantum_Sampler(2, w, x, b, workflow="simulated")
            annealed = rnn_sampler.execute()
            score += compare_answers(annealed, 2, w, x, b)

    print(score/((iterations - 1)*subtests))




