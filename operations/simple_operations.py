from utils.variables import c_summation
from logic_gates.quantum_gates import xnor


"""
Operands do not contain target!!!
"""


def weak_summation(bqm, operands):
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


def quantum_sigmoid_sum(bqm, operands, name_target):
    """
    it sets the operands force fields, to later apply weak summation
    and strong summation

    :param operands: dictionary with qubits names -> real value (force-fields)
    :param name_target: string, qubit name where the result is saved
    :return: bqm
    """

    for key, value in operands.items():
        bqm.add_variable(key, -value)

    # put target in perfect superposition state
    bqm.add_variable(name_target, 0.0)

    weak_summation(bqm, operands)
    strong_summation(bqm, operands, name_target)


def multiplication(bqm, name1, name2, val1, val2):
    return xnor(bqm, name1, name2, val1, val2)


# matrix operations


def matrix_vector_multiplication(bqm, matrix_names, weights, arr_names, arr_value=None):
    if arr_value is None:
        arr_value = [0.0 for _ in range(len(weights[0]))]
    assert len(matrix_names[0]) == len(arr_names)

    operands = dict()
    for i in range(len(matrix_names)):
        for j in range(len(matrix_names)):
            bqm.add_variable(matrix_names[i][j], weights[i][j])
            bqm.add_variable(arr_names[j], arr_value[j])
            temp_res = multiplication(matrix_names[i][j], arr_names[j], weights[i][j], arr_value[j])
            operands[temp_res[0]] = weights[i][j]
    return operands
