'''
~1,000,000 Pauli terms
~300 logical qubits
~10^9 circuit evaluations

solving it would likely be a Nobel Prize–level result.
'''

###############################################################
# FeMoco VQE Simulation using Eclipse Qrisp
# Full Active Space (~108 spin orbitals)
###############################################################

from pyscf import gto
from qrisp import QuantumVariable
from qrisp.vqe.problems.electronic_structure import *

###############################################################
# FeMoco Geometry (approximate)
###############################################################

femoco_geometry = '''
Mo      0.000   0.000   0.000
Fe      2.630   0.000   0.000
Fe     -2.630   0.000   0.000
Fe      0.000   2.630   0.000
Fe      0.000  -2.630   0.000
Fe      1.800   1.800   1.800
Fe     -1.800  -1.800   1.800
Fe      1.800  -1.800  -1.800
S       3.800   1.000   0.000
S      -3.800  -1.000   0.000
S       1.000   3.800   0.000
S      -1.000  -3.800   0.000
S       0.000   0.000   3.500
S       0.000   0.000  -3.500
C       0.000   0.000   0.800
'''

###############################################################
# Build PySCF Molecule
###############################################################

mol = gto.M(
    atom=femoco_geometry,
    basis='sto-3g',
    charge=0,
    spin=0
)

print("Electrons:", mol.nelectron)

###############################################################
# Create Qrisp Electronic Structure Problem
###############################################################

vqe = electronic_structure_problem(mol)

###############################################################
# Automatski Quantum Backend
###############################################################

import sys
sys.path.append('../../')

from AutomatskiKomencoQiskit import AutomatskiKomencoQiskit
from AutomatskiBackendQrisp import *

backend = AutomatskiKomencoQiskit(
    host="xxx.xxx.xxx.xxx",
    port=xx
)

automatski_backend = AutomatskiBackend(
    backend=backend
)

###############################################################
# Allocate Qubits
###############################################################

# 108 spin orbitals → 108 qubits
qv = QuantumVariable(108)

print("Allocated qubits:", len(qv))

###############################################################
# Run VQE
###############################################################
vqe.set_callback()

energy = vqe.run(
    qv,
    depth=2,
    max_iter=100,
    mes_kwargs={
        "backend": automatski_backend
    }
)

print("\nEstimated FeMoco Ground State Energy")
print(energy)

vqe.visualize_energy(exact=False)
