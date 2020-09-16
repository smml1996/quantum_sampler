import dimod
import string
from dwave.system import DWaveSampler
from dwave.cloud import Client
import neal

# Proposal constants
c_y = 100.0
c_summation = 0.8
c_xnor = -0.25

# utils
letters = string.ascii_letters
abs_numbers_range = 100000
qpu = DWaveSampler(solver={'qpu': True})
simulated_sampler = neal.SimulatedAnnealingSampler()

# Chimera Graph Architecture
chimera_columns = 16
chimera_rows = 16
tile_shores = 4
