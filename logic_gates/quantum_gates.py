from utils.variables import c_xnor


def quantum_not(bqm, name, val1):
    new_name = "n-" + name
    bqm.add_variable(new_name, 2*val1)
    return [new_name]


def xnor(bqm, name1, name2, w, x=0.0, c_reinforcement=c_xnor):
    # define names for ancillas
    name_ancilla1 = "an1-" + name1 + "-" + name2
    name_ancilla2 = "an2-" + name1 + "-" + name2

    # define name for result
    name_res = "xnor-r-"+name1+name2

    # add operands
    bqm.add_variable(name1, -2*w)
    bqm.add_variable(name2, -2*x)

    # add and define negated operands
    negated1 = quantum_not(name1, w)[0]
    negated2 = quantum_not(name2, x)[0]

    # add ancillas
    bqm.add_variable(name_ancilla1, -abs(w))
    bqm.add_variable(name_ancilla2, -abs(w))

    # add result
    bqm.add_variable(name_res, -abs(w))

    # connect negated operands with first ancilla
    bqm.add_interaction(negated1, name_ancilla1, abs(w))
    bqm.add_interaction(negated2, name_ancilla1, abs(w))

    # connect operands with second ancilla
    bqm.add_interaction(name1, name_ancilla2, abs(w))
    bqm.add_interaction(name2, name_ancilla2, abs(w))

    # connect ancillas with result
    bqm.add_interaction(name_ancilla1, name_res, abs(w))
    bqm.add_interaction(name_ancilla2, name_res, abs(w))

    # reinforce ancillas
    bqm.add_interaction(name_ancilla1, name_ancilla1, c_reinforcement)

    return [name_res]

