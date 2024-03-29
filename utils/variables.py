import dimod
import string
from dwave.system import DWaveSampler
from dwave.cloud import Client
import neal

# Proposal constants
# best c_y = 100000000 -> 0.84
c_y = 10000000000
c_summation = 0.25
c_xnor = -0.25
c_t = -1000000.0

# utils
letters = string.ascii_letters
abs_numbers_range = 10000
qpu = DWaveSampler(solver={'qpu': True})
simulated_sampler = neal.SimulatedAnnealingSampler()

# Chimera Graph Architecture
chimera_columns = 16
chimera_rows = 16
tile_shores = 4
