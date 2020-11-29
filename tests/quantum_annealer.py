from dwave.system import EmbeddingComposite

from quantum_sampler.quantum_sampler import Quantum_Sampler
from utils.tools import get_random_matrix, compare_answers, evaluate_rnn
from classical_sampler.sampler import Sampler
from utils.variables import qpu


def test1():
    f = open('./results/temp.csv', "w")
    f.write("m,prob_annealed,prob_random,real\n")
    '''
    using simple connection between timesteps
    :return:
    '''
    score = 0
    score_beam = 0
    iterations = 6
    subtests = 10
    timesteps = 2
    beam_sampler = Sampler()
    probs_beam = 0.0
    probs_anneal = 0.0
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
            #print("len real: ",len(temp_real))
            rnn_sampler = Quantum_Sampler(timesteps, w, x, b, workflow="simulated")
            annealed = rnn_sampler.execute()
            # print(annealed)
            #print( "print reversed: ",Sampler().decode_reverse(w,x,b, annealed))
            #print(annealed)
            temp_prob_anneal = Sampler().decode_reverse(w,x,b, annealed)
            probs_anneal += temp_prob_anneal
            print('annealed: ', temp_prob_anneal)
            real = temp_real
            print('real: ', real[0].probability)
            beam = beam_sampler.sample(w, x, b, timesteps, beam_size=1 )[0]
            print('beam: ',  beam.probability)
            print('')
            probs_beam += beam.probability
            temp = compare_answers(annealed, real)
            temp2 = compare_answers(beam, real)
            score_sub_beam += temp2
            score_subtests += temp
            score += temp
            score_beam += temp2
            f.write(str(m) +","+ str(temp_prob_anneal) +"," + str(beam.probability) + "," + str(real[0].probability) + "\n")
        score_subtests /= subtests
        score_sub_beam /= subtests
        print(score_subtests)
        print("score sub beam: ", score_sub_beam )
    print(score/((iterations - 1)*subtests))
    print("prob anneal", probs_anneal)
    print("score beam", score_beam/((iterations - 1)*subtests))
    print("prob beam", probs_beam)

    f.close()

def test2():
    f = open('./results/temp.csv', "w")
    f.write("m,prob_annealed,prob_random,real\n")
    '''
    using simple connection between timesteps
    :return:
    '''
    score = 0
    score_beam = 0
    iterations = 6
    subtests = 1
    timesteps = 2
    beam_sampler = Sampler()
    probs_beam = 0.0
    probs_anneal = 0.0
    for m in range(512, 1025, 512):
        score_subtests = 0
        score_sub_beam = 0
        for i in range(subtests):
            w = get_random_matrix(m, m)
            w = w[1]

            x = get_random_matrix(1, m, True)
            x = x[1][0]

            b = get_random_matrix(1, m, False)
            b = b[1][0]
            #temp_real = Sampler().sample(w, x, b, timesteps, -1)
            # print("len real: ",len(temp_real))
            rnn_sampler = Quantum_Sampler(timesteps, w, x, b, workflow="kerberos")
            print("finish building model")
            annealed = rnn_sampler.execute()
            # print( "print reversed: ",Sampler().decode_reverse(w,x,b, annealed))
            print("sampler done")

            temp_prob_anneal = Sampler().decode_reverse(w, x, b, annealed)
            probs_anneal += temp_prob_anneal
            print('annealed: ', temp_prob_anneal)
            #real = temp_real
            #print('real: ', real[0].probability)
            beam = beam_sampler.sample(w, x, b, timesteps, beam_size=1)[0]
            print('beam: ', beam.probability)
            print('')
            probs_beam += beam.probability
            #temp = compare_answers(annealed, real)
            #temp2 = compare_answers(beam, real)
            #score_sub_beam += temp2
            #score_subtests += temp
            #score += temp
            #score_beam += temp2
            f.write(str(m) + "," + str(temp_prob_anneal) + "," + str(beam.probability) + "\n")
        score_subtests /= subtests
        score_sub_beam /= subtests
        print(score_subtests)
        print("score sub beam: ", score_sub_beam)
    print(score / ((iterations - 1) * subtests))
    print("prob anneal", probs_anneal)
    print("score beam", score_beam / ((iterations - 1) * subtests))
    print("prob beam", probs_beam)

    f.close()


def test3():
    f = open('./results/temp.csv', "w")
    f.write("m,prob_annealed,prob_random,real,random\n")
    '''
    using simple connection between timesteps
    :return:
    '''
    score = 0
    score_beam = 0
    score_random = 0
    iterations = 5
    subtests = 5
    timesteps = 2
    beam_sampler = Sampler()
    probs_beam = 0.0
    probs_random = 0.0
    probs_anneal = 0.0
    for m in range(2, iterations+1):
        score_subtests = 0
        score_sub_beam = 0
        score_sub_random = 0
        for i in range(subtests):
            w = get_random_matrix(m, m)
            w = w[1]

            x = get_random_matrix(1, m, True)
            x = x[1][0]

            b = get_random_matrix(1, m, False)
            b = b[1][0]
            temp_real = Sampler().sample(w, x, b, timesteps, -1)
            #print("len real: ",len(temp_real))
            rnn_sampler = Quantum_Sampler(timesteps, w, x, b, workflow="simulated")
            read_values = rnn_sampler.build_model()
            sampler = EmbeddingComposite(qpu)
            result = sampler.sample(rnn_sampler.bqm, num_reads=10, chain_strength=1000).first.sample
            annealed = rnn_sampler.read_result(result, read_values)
            print(annealed)
            # print(annealed)
            #print( "print reversed: ",Sampler().decode_reverse(w,x,b, annealed))
            #print(annealed)
            temp_prob_anneal = Sampler().decode_reverse(w,x,b, annealed)
            probs_anneal += temp_prob_anneal

            print('annealed: ', temp_prob_anneal)
            real = temp_real
            print('real: ', real[0].probability)
            beam = beam_sampler.sample(w, x, b, timesteps, beam_size=1 )[0]
            print('beam: ',  beam.probability)
            random = beam_sampler.sample(w, x, b, timesteps, beam_size=1, is_sort=False)[0]
            print('random: ', random.probability)
            print('')
            probs_beam += beam.probability
            probs_random += random.probability
            temp = compare_answers(annealed, real)
            temp2 = compare_answers(beam, real)
            temp3 = compare_answers(random, real)
            score_sub_beam += temp2
            score_subtests += temp
            score_sub_random += temp3
            score += temp
            score_beam += temp2
            score_random+= temp3
            f.write(str(m) +","+ str(temp_prob_anneal) +"," + str(beam.probability) + "," + str(real[0].probability)+","+str(random.probability) + "\n")
        score_subtests /= subtests
        score_sub_beam /= subtests
        score_sub_random /= subtests
        print("score sub anneal",score_subtests)
        print("score sub beam: ", score_sub_beam )
        print("score sub random: ", score_sub_random)

    print("prob anneal", probs_anneal)
    print("prob beam", probs_beam)
    print("prob random", probs_random)
    print("score anneal",score / ((iterations - 1) * subtests))
    print("score beam", score_beam/((iterations - 1)*subtests))
    print("score random", score_random/ ((iterations - 1) * subtests))







