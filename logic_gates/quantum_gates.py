from utils.variables import c_xnor
import dimod

def quantum_not(bqm, name, val1):
    new_name = "n-" + name
    bqm.add_variable(new_name, val1)

    # force qubits to have diff. signs
    #bqm.add_interaction(new_name, name, 0.25)

    return [new_name]


def xnor(bqm, name1, name2, w, x=-1, c_reinforcement=c_xnor, unknown_x=False, previous_x=None, c_t=None):
    # turn variable x propitious to Ising model
    if not unknown_x:
        if x <= 0:
            x = -1
        else:
            x = 1

    # define names for ancillas
    name_ancilla1 = "an1-" + name1 + "-" + name2
    name_ancilla2 = "an2-" + name1 + "-" + name2

    # define name for result
    name_res = "xnor-r-"+name1+name2

    # add operands
    bqm.add_variable(name1, -2*w)

    bqm.add_variable(name2, -2 * x * abs(w))



    # add and define negated operands
    negated1 = quantum_not(bqm, name1, 2*w)[0]
    negated2 = quantum_not(bqm, name2, 2* x * abs(w))[0]
    #if unknown_x:
    #    bqm.add_interaction(negated2, previous_x, -c_t)

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
    bqm.add_interaction(name_ancilla1, name_ancilla2, c_reinforcement)

    return [name_res]

