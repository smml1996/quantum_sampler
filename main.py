# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from logic_gates.quantum_gates import quantum_not
from random import seed
from tests.simple_operations import longest_run_sum, sum_simulated_test, quantum_mult_sum, simulated_mult_sum_avg
from utils.variables import qpu
from tests.simple_operations import sign_extraction_test, quantum_sign_test, simulated_mult_sum
# from tests.simple_operations import sum_quantum_test
from quantum_sampler.quantum_sampler import Quantum_Sampler
from tests.quantum_annealer import test1, test2

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print(qpu.sampler)
    seed(7)
    # TESTS

    # longest_run_sum()

    # sum_simulated_test()
    # sum_quantum_test()

    # sign_extraction_test()
    # quantum_sign_test()

    # simulated_mult_sum()
    # simulated_mult_sum_avg()
    # quantum_mult_sum()
    # qs = Quantum_Sampler(1, [[1]], [1], [1])
    # qs.execute()
    test1()
    # test2()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
