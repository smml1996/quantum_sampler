from utils import variables
from utils.tools import get_bqm
from utils.tools import get_names
from operations.simple_operations import quantum_sigmoid_sum, multiplication, matrix_vector_multiplication
import hybrid
from hybrid.reference.kerberos import KerberosSampler

class Quantum_Sampler:
    def __init__(self, timesteps, weights, x_t0, bias,
                 c_summation=variables.c_summation, c_xnor=variables.c_xnor, c_y=variables.c_y, convergence=3, type="workflow1"):
        self.timesteps = timesteps
        self.weights = weights
        self.x = x_t0
        self.x_superposition = [0 for _ in self.x]
        self.bias = bias
        self.c_summation = c_summation
        self.c_xnor = c_xnor
        self.c_y = c_y
        self.bqm = get_bqm()
        self.convergence = convergence
        self.type = type

    def build_t0(self):
        prefix = "t0"
        matrix_names = get_names(self.weights, prefix + "w")
        x_names = get_names(self.x, prefix+"x")
        x_names = x_names[0]

        # perform multiplication
        operands = matrix_vector_multiplication(self.bqm, matrix_names, self.weights, x_names, arr_value=self.x)[0]
        x_next = []

        # perform summation
        for i in range(len(operands)):
            quantum_sigmoid_sum(self.bqm, operands[i], "t0_target" + str(i), set_operands=False)
            x_next.append("t0_target" + str(i))

        # ensure to pick one
        for i in range(len(x_next)):
            for j in range(i+1, len(x_next)):
                self.bqm.add_interaction(x_next[i], x_next[j], self.c_y)

        return x_next

    def build_t(self, x_names, t_index):
        prefix = str(t_index)
        xt = [0 for _ in self.x]
        # x_names = get_names(xt, prefix + "x")
        # x_names = x_names[0]
        matrix_names = get_names(self.weights, prefix + "w")

        # perform multiplication
        operands = matrix_vector_multiplication(self.bqm, matrix_names, self.weights, x_names, arr_value=xt)[0]
        x_next = []

        # perform summation
        for i in range(len(operands)):
            quantum_sigmoid_sum(self.bqm, operands[i], prefix + "_target" + str(i), set_operands=False)
            x_next.append(prefix + "_target" + str(i))

        # ensure to pick one
        for i in range(len(x_next)):
            for j in range(i+1, len(x_next)):
                self.bqm.add_interaction(x_next[i], x_next[j], self.c_y)
        return x_next

    def join_steps(self, prev, next):
        for i in range(len(prev)):
            self.bqm.add_interaction(prev[i], next[i], self.c_y)

    def build_model(self):
        read_values = []
        x_next = self.build_t0()
        read_values.append(x_next)
        for i in range(self.timesteps-1):
            prefix = str(i+1)
            x_names = get_names([0 for _ in self.x], prefix + "x")
            x_names = x_names[0]
            self.join_steps(x_next, x_names)
            x_next = self.build_t(x_names, i)
            read_values.append(x_next)
        return read_values

    def execute(self):

        if type == 'workflow1':
            subproblem = hybrid.EnergyImpactDecomposer(size=60)
            subsampler = hybrid.QPUSubproblemAutoEmbeddingSampler() | hybrid.SplatComposer()

            iteration = hybrid.RacingBranches(
                hybrid.InterruptableTabuSampler(),
                subproblem | subsampler
            ) | hybrid.ArgMin()

            workflow = hybrid.LoopUntilNoImprovement(iteration, convergence=self.convergence)

            init_state = hybrid.State.from_problem(self.bqm)
            result = workflow.run(init_state).result().samples.first
            return result
        elif type == 'kerberos':
            result = KerberosSampler().sample(self.bqm)
            return result
        else:
            raise Exception("not valid sampler. Valid options: workflow1, kerberos")