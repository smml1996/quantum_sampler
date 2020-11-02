from utils import variables

from logic_gates.quantum_gates import xnor


"""
Operands do not contain target!!!
"""


def weak_summation(bqm, operands, c_summation=variables.c_summation):
    """
    This function uses an environment variable c_summation that ensures
    that make qubits "agree" with each other.

    Assumes that qubit force-field is already set.

    :param operands: dictionary with qubits names -> real value (force field value)
    :return: bqm with entanglement between operands
    """
    temp_operands = list(operands.items())
    for i in range(len(temp_operands)):
        for j in range(i + 1, len(temp_operands)):
            bqm.add_interaction(temp_operands[i][0], temp_operands[j][0], c_summation)


def strong_summation(bqm, operands, target):
    """
    This uses the own qubit weight to establish entanglement towards a target qubit.

    Assumes that qubit force-field is already set.

    :param operands:  dictionary with qubits names -> real value (force-fields)
    :param target: string, qubit name where the result is saved
    :return: bqm with entanglements between operands and target qubit
    """
    for key, value in operands.items():
        if key != target:
            bqm.add_interaction(key, target, -abs(value))


def quantum_sigmoid_sum(bqm, operands, name_target, set_operands=True, c_summation=variables.c_summation):
    """
    it sets the operands force fields, to later apply weak summation
    and strong summation

    :param c_summation:
    :param set_operands:
    :param operands: dictionary with qubits names -> real value (force-fields)
    :param name_target: string, qubit name where the result is saved
    :return: bqm
    """
    if set_operands:
        for key, value in operands.items():
            bqm.add_variable(key, -value)

    # put target in perfect superposition state
    bqm.add_variable(name_target, 0.0)

    weak_summation(bqm, operands, c_summation=c_summation)
    strong_summation(bqm, operands, name_target)


def multiplication(bqm, name1, name2, val1, val2, c_reinforcement=variables.c_xnor):
    return xnor(bqm, name1, name2, val1, val2, c_reinforcement)


# matrix operations
def matrix_vector_multiplication(bqm, matrix_names, weights, arr_names, arr_value=None, c_reinforcement=variables.c_xnor):
    if arr_value is None:
        arr_value = [0.0 for _ in range(len(weights[0]))]
    print(len(matrix_names[0]), len(arr_names))
    assert len(matrix_names[0]) == len(arr_names)

    result = []

    for i in range(len(matrix_names)):
        operands = dict()
        for j in range(len(matrix_names[0])):
            # bqm.add_variable(matrix_names[i][j], weights[i][j])
            # bqm.add_variable(arr_names[j], arr_value[j])
            temp_res = multiplication(bqm, matrix_names[i][j], arr_names[j], weights[i][j], arr_value[j],
                                      c_reinforcement=c_reinforcement)
            operands[temp_res[0]] = weights[i][j]

        result.append(operands)
    # return [operands]
    return [result]
