from quantum_sampler.quantum_sampler import Quantum_Sampler
from utils.tools import get_random_matrix, compare_answers, evaluate_rnn
from classical_sampler.sampler import Sampler

def test1():
    '''
    using simple connection between timesteps
    :return:
    '''
    score = 0
    score_beam = 0
    iterations = 6
    subtests = 10
    timesteps = 3
    beam_sampler = Sampler()
    for m in range(2, iterations+1):
        score_subtests = 0
        score_sub_beam = 0
        for i in range(subtests):
            w = get_random_matrix(m, m)
            w = w[1]

            x = get_random_matrix(1, m, True)
            x = x[1][0]

            b = get_random_matrix(1, m, False)
            b = b[1][0]
            temp_real = Sampler().sample(w, x, b, timesteps, -1)
            rnn_sampler = Quantum_Sampler(timesteps, w, x, b, workflow="simulated")
            # print(Sampler().sample(w, x, b, 2, -1))
            annealed = rnn_sampler.execute()
            print('annealed: ', annealed, Sampler().get_probability(annealed, temp_real))
            real = temp_real[0]
            print('real: ', real.outputs, real.probability)
            beam = beam_sampler.sample(w, x, b, timesteps, beam_size=1, is_sort=False)[0]
            print('beam: ', beam.outputs, real.probability)
            temp = compare_answers(annealed, real)
            temp2 = compare_answers(beam, real)
            score_sub_beam += temp2
            score_subtests += temp
            score += temp
            score_beam += temp2
        score_subtests /= subtests
        score_sub_beam /= subtests
        print(score_subtests)
        print("score sub beam: ", score_sub_beam )
    print(score/((iterations - 1)*subtests))
    print("score beam", score_beam/((iterations - 1)*subtests))


def test2():
    '''
    using simple connection between timesteps
    :return:
    '''
    score = 0
    iterations = 100
    subtests = 10

    for m in range(2, iterations + 1):
        score_subtests = 0
        for i in range(subtests):
            w = get_random_matrix(m, m)
            w = w[1]

            x = get_random_matrix(1, m, True)
            x = x[1][0]

            b = get_random_matrix(1, m, False)
            b = b[1][0]

            rnn_sampler = Quantum_Sampler(3, w, x, b, workflow="kerberos")
            annealed = rnn_sampler.execute()
            temp = compare_answers(annealed, 2, w, x, b)
            score_subtests += temp
            score += temp
        score_subtests /= subtests
        print("score subtests: ", score_subtests)
        print("temp score: ", score / ((m - 1) * subtests))
    print(score / ((iterations - 1) * subtests))

def test3():
    score = 0
    iterations = 100
    subtests = 5

    m = 512
    score_subtests = 0
    beam_sampler = Sampler()
    for i in range(subtests):
        w = get_random_matrix(m, m)
        w = w[1]

        x = get_random_matrix(1, m, True)
        x = x[1][0]

        b = get_random_matrix(1, m, False)
        b = b[1][0]
        rnn_sampler = Quantum_Sampler(3, w, x, b, workflow="kerberos")
        annealed = rnn_sampler.execute()
        annealed_prob = beam_sampler.get_probability(annealed, w,x, b)
        beam = beam_sampler.sample(w, x, b, 12, 1)[0]
        # temp = compare_answers(annealed, 2, w, x, b)
        # score_subtests += temp
        # score += temp




