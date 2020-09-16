from utils.tools import get_bqm, get_random_dict, get_simulated_sampler
from dwave.embedding.chimera import find_clique_embedding
from dwave.system import FixedEmbeddingComposite
import dimod
from utils.variables import qpu, chimera_columns, chimera_rows, tile_shores
from operations.simple_operations import quantum_sigmoid_sum
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
    f = open("./results/simulated_sigmoid_sum.txt", "w")
    f.write("num. of qubits; precision\n")

    computable_qubits = 27
    num_subtest = 1000

    for i in range(2, computable_qubits):
        print("qubit: ", i)
        precision = 0
        x = []
        for j in range(num_subtest):

            random_dict = get_random_dict(i)

            # compute real answer
            real_answer = 0
            for value in random_dict.values():
                real_answer += value

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
            elif real_answer == result.first.sample['target']:
                precision += 1

        precision /= num_subtest
        print(x)
        f.write(str(i) + ";" + str(precision) + ";"+ str(statistics.variance(x)) +"\n")
    f.close()


def sum_quantum_test():
    # 0.8 c_summation, 100000
    f = open("./results/quantum_sigmoid_sum.txt", "w")
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


def multiplication_test():
    pass
