from utils.tools import get_bqm, get_random_dict, get_simulated_sampler, get_random_number
from utils.tools import get_random_matrix
from dwave.embedding.chimera import find_clique_embedding
from dwave.system import FixedEmbeddingComposite, EmbeddingComposite, AutoEmbeddingComposite
import dimod
from utils.variables import qpu, chimera_columns, chimera_rows, tile_shores, abs_numbers_range, c_xnor
from utils import variables
from operations.simple_operations import quantum_sigmoid_sum, multiplication, matrix_vector_multiplication
import statistics


def longest_run_sum():
    f = open("./results/longest_run.txt", "w")
    f.write("num. of qubits;longest chain\n")
    for i in range(2, 64):
        bqm = dimod.BinaryQuadraticModel.empty(dimod.BINARY)
        random_dict = get_random_dict(i)
        for key, value in random_dict.items():
            bqm.add_variable(key, value)
        embedding = find_clique_embedding(bqm.variables,
                                          # size of the chimera lattice
                                          chimera_rows,
                                          chimera_columns,
                                          tile_shores,  # size of shore within each tile
                                          target_edges=qpu.edgelist)

        max_chain = max(len(x) for x in embedding.values())
        f.write(str(i) + ";" + str(max_chain) + "\n")
    f.close()


def sum_simulated_test():
    """
     computable qubits = (2^x <= 10^9) --> (x = 27)
    :return: None
    """
    f = open("./results/simulated_sigmoid_sum.csv", "w")
    #f1 = open("./results/avg_pres.txt", "w")
    #f.write("num. of qubits; precision\n")


    computable_qubits = 18
    num_subtest = 10

    acum_precision = 0
    coeffs = []
    temp = -10
    while temp < 11:
        coeffs.append(temp)
        temp += 0.25
    #for coeff in coeffs:
    #    variables.c_summation = coeff
    #    print(coeff)
    for i in range(2, computable_qubits):
        #print("qubit: ", i)
        precision = 0
        x = []
        for j in range(num_subtest):

            random_dict = get_random_dict(i)

            # compute real answer
            real_answer = 0
            for value in random_dict.values():
                real_answer += value
            # f1.write(str(real_answer)+";")
            x.append(real_answer)

            # assign spin value to real_answer
            if real_answer < 0:
                real_answer = -1
            elif real_answer > 0:
                real_answer = 1
            else:
                real_answer = 0
            bqm = get_bqm()
            quantum_sigmoid_sum(bqm, random_dict, "target")
            sampler = get_simulated_sampler()
            result = sampler.sample(bqm)
            if real_answer == 0:
                precision += 1
                # f1.write("1\n")
            elif real_answer == result.first.sample['target']:
                precision += 1
                # f1.write("1\n")
#            else:
                # f1.write("0\n")

        precision /= num_subtest
        # acum_precision+= precision

        f.write(str(i) + ";" + str(precision) + "\n")
    f.close()
        #f1.write(str(coeff)+";"+ str(round(acum_precision/(computable_qubits-1), 4)) + "\n")
     #   acum_precision = 0
    #f1.close()


def sum_quantum_test():
    # 0.8 c_summation, 100000
    f = open("./results/quantum_sigmoid_sum.csv", "w")
    f.write("num. of qubits; precision\n")
    num_subtest = 10
    for i in range(40, 63):
        print("qubit: ", i)
        precision = 0
        for j in range(num_subtest):

            random_dict = get_random_dict(i)

            # compute real answer
            real_answer = 0
            for value in random_dict.values():
                real_answer += value

            # assign spin value to real_answer
            if real_answer < 0:
                real_answer = -1
            elif real_answer > 0:
                real_answer = 1
            else:
                precision += 1
                continue

            bqm = get_bqm()
            quantum_sigmoid_sum(bqm, random_dict, "target")

            embedding = find_clique_embedding(bqm.variables,
                                              16, 16, 4,  # size of the chimera lattice
                                              target_edges=qpu.edgelist)
            qpu_sampler = FixedEmbeddingComposite(qpu, embedding)
            result = qpu_sampler.sample(bqm, num_reads=100)
            if real_answer == 0:
                precision += 1
            elif real_answer == result.first.sample['target']:
                precision += 1
        precision /= num_subtest

        print(precision)
        f.write(str(i) + ";" + str(precision) + "\n")
    f.close()


def sign_extraction_test():
    total_test = 10000
    precision = 0

    coeffs = []
    start = -20
    f_avg = open("./results/simulated_mult_avg_pres.csv", "w")
    while start <= 10:
        coeffs.append(start)
        start += 0.25

    for coeff in coeffs:
        precision = 0
        print(coeff)
        for i in range(total_test):
            bqm = get_bqm()

            w = get_random_number()
            x = get_random_number()
            expected = 1

            if w * x < 0:
                expected = -1
            elif w * x == 0:
                precision += 1
                continue

            name_res = multiplication(bqm, 'name1', 'name2', w, x, c_reinforcement=coeff)[0]
            sampler = get_simulated_sampler()
            result = sampler.sample(bqm)
            if result.first.sample[name_res] == expected:
                precision += 1
            # print(precision)

        precision /= total_test
        print(precision)
        f_avg.write(str(coeff) + ";" +str(round(precision, 3)))
    #f = open("./results/simulated_mult.csv", "a")
    #f.write("\n"+str(abs_numbers_range) + ";" + str(c_xnor) + ";" + str(precision))
    #f.close()


def quantum_sign_test():
    total_test = 10
    precision = 0
    for i in range(total_test):
        print(i+1, precision)
        bqm = get_bqm()
        w = get_random_number()
        x = get_random_number()

        expected = 1

        if w * x < 0:
            expected = -1
        elif w * x == 0:
            precision += 1
            continue
        name_res = multiplication(bqm, 'w', 'x', w, x)[0]

        sampler = EmbeddingComposite(qpu)

        result = sampler.sample(bqm, num_reads=1000)

        if expected == result.first.sample[name_res]:
            precision += 1

    precision /= total_test
    f = open("./results/quantum_mult.csv", "a")
    f.write("\n"+str(abs_numbers_range) + ";" + str(c_xnor) + ";" + str(precision))
    f.close()


def simulated_mult_sum():
    f = open("./results/simulated_mult_sum.csv", "w")
    f.write("num_subtests;m;precision\n")

    f1 = open("./results/energy.csv", "w")
    f1.write("energy;num_occurrences")

    num_subtests = 10
    for i in range(2, 5):
        precision = 0
        f1.write("###### " + str(i) +" ######\n")
        for j in range(num_subtests):
            bqm = get_bqm()
            m = i
            matrix_names, weights = get_random_matrix(1, m, False)
            x_names, x = get_random_matrix(1, m, True)
            x_names = x_names[0]
            x = x[0]

            real_result = 0
            for ii in range(m):
                real_result += weights[0][ii] * x[ii]

            if real_result < 0:
                real_result = -1
            elif real_result > 0:
                real_result = 1
            else:
                precision += 1
                continue

            operands = matrix_vector_multiplication(bqm, matrix_names, weights, x_names, arr_value=x)[0]

            quantum_sigmoid_sum(bqm, operands, "target", set_operands=False)
            sampler = get_simulated_sampler()

            result = sampler.sample(bqm, num_reads=1000)

            if result.first.sample["target"] == real_result:
                precision += 1
            f1.write(str(result.first.energy) + ";"+ str(result.first.num_occurrences) + "\n")
        print(precision/num_subtests)
        f.write(str(num_subtests) + ";" + str(i) + ";" + str(precision/num_subtests) + "\n")


def simulated_mult_sum_avg():
    f = open("./results/simulated_mult_sum_avg.csv", "w")
    f.write("x;y;z\n")

    coeffs = []
    temp = -5
    while temp<=5:
        coeffs.append(temp)
        temp+=0.25
    num_subtests = 10

    accum_precision = 0

    for c1 in coeffs:
        print("$$$$$$$$$$$$$$")
        for c2 in coeffs:
            print(c1, c2)
            accum_precision = []
            for i in range(2, 5):

                precision = 0

                for j in range(num_subtests):
                    bqm = get_bqm()
                    m = i
                    matrix_names, weights = get_random_matrix(1, m, False)
                    x_names, x = get_random_matrix(1, m, True)
                    x_names = x_names[0]
                    x = x[0]

                    real_result = 0
                    for ii in range(m):
                        real_result += weights[0][ii] * x[ii]

                    if real_result < 0:
                        real_result = -1
                    elif real_result > 0:
                        real_result = 1
                    else:
                        precision += 1
                        continue

                    operands = matrix_vector_multiplication(bqm, matrix_names, weights, x_names, arr_value=x, c_reinforcement=c1)[0]

                    quantum_sigmoid_sum(bqm, operands, "target", set_operands=False, c_summation=c2)
                    sampler = get_simulated_sampler()

                    result = sampler.sample(bqm, num_reads=1000)

                    if result.first.sample["target"] == real_result:
                        precision += 1
                precision /= num_subtests
                accum_precision.append(precision)
            f.write(str(c2) + ";" + str(c1) + ";" + str(statistics.mean(accum_precision)) + "\n")


def quantum_mult_sum():
    f = open("./results/quantum_mult_sum.csv", "w")
    f.write("num_subtests;m;precision\n")
    # f1 = open("./results/quantum_energy.csv", "w")
    # f1.write("precision;energy;occurences\n")
    num_subtests = 10
    for i in range(2, 10):
        precision = 0
        for j in range(num_subtests):
            bqm = get_bqm()
            m = i
            matrix_names, weights = get_random_matrix(1, m, False)
            x_names, x = get_random_matrix(1, m, True)
            x_names = x_names[0]
            x = x[0]

            real_result = 0
            for ii in range(m):
                real_result += weights[0][ii] * x[ii]

            if real_result < 0:
                real_result = -1
            elif real_result > 0:
                real_result = 1
            else:
                precision += 1
                continue

            operands = matrix_vector_multiplication(bqm, matrix_names, weights, x_names, arr_value=x)[0]

            quantum_sigmoid_sum(bqm, operands, "target", set_operands=False)
            sampler = EmbeddingComposite(qpu)

            result = sampler.sample(bqm, num_reads=1200)

            if result.first.sample["target"] == real_result:
                precision += 1
                #f1.write("1;")
            #else:
            #    f1.write("0;")
                # print(real_result, result.first.sample["target"], result)
            #f1.write(str(result.first.energy))
            #f1.write(";"+str(result.first.num_occurrences/1000*100)+"\n")
        print(precision/num_subtests)
        f.write(str(num_subtests) + ";" + str(i) + ";" + str(precision/num_subtests) + "\n")