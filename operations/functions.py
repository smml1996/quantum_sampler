from utils import variables


def quantum_arg_max(bqm, operands, c_y=variables.c_y):

    '''
    :param operands: list of operands (names)
    :return:
    '''

    for operand1 in operands:
        for operand2 in operands:
            if operand1 != operand2:
                bqm.add_interaction(operand1, operand2, c_y)