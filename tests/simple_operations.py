from utils.tools import clean_workspace, get_random_dict
from dwave.embedding.chimera import find_clique_embedding
import dimod
from utils.variables import qpu, chimera_columns, chimera_rows, tile_shores
from operations.simple_operations import quantum_sigmoid_sum


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


def sum_test():
    bqm = dimod.BinaryQuadraticModel.empty(dimod.BINARY)
    random_dict = get_random_dict(2)
