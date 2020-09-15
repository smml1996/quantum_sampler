class Quantum_Sampler:
    def __init__(self, timesteps, weights, x_t0, bias):
        self.timesteps = timesteps
        self.weights = weights
        self.x = x_t0
        self.bias = bias