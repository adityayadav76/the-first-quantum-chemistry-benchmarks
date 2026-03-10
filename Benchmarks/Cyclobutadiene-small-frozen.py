'''
pip install qrisp
pip install pyscf
pip install openfermion
pip install openfermionpyscf
pip install scipy
'''

from pyscf import gto
from qrisp import QuantumVariable
from qrisp.vqe.problems.electronic_structure import *

# ============================================================
# 1. Define Molecule (Cyclobutadiene)
# ============================================================

mol = gto.M(
    atom = '''
    C  0.0000  1.0000 0.0000
    C  1.0000  0.0000 0.0000
    C  0.0000 -1.0000 0.0000
    C -1.0000  0.0000 0.0000
    H  0.0000  2.0000 0.0000
    H  2.0000  0.0000 0.0000
    H  0.0000 -2.0000 0.0000
    H -2.0000  0.0000 0.0000
    ''',
    basis = 'sto-3g',
    charge = 0,
    spin = 0
)

# ============================================================
# 2. Build Electronic Structure Problem
# ============================================================

vqe = electronic_structure_problem(
    mol,
    freeze_core=True,     # freeze deep orbitals
    active_orbitals=12    # 12 spatial orbitals → 24 qubits
)

# ============================================================
# 3. Define Quantum Register
# ============================================================

n_qubits = 24
qv = QuantumVariable(n_qubits)

# ============================================================
# 4. Optional: Connect Your Backend
# ============================================================

import sys
sys.path.append('../../python/')

from AutomatskiKomencoQiskit import AutomatskiKomencoQiskit
from AutomatskiBackendQrisp import *

backend = AutomatskiKomencoQiskit(
    host="XXX.XXX.XXX.XXX",
    port=XX
)

automatski_backend = AutomatskiBackend(backend=backend)

# ============================================================
# 5. Run VQE
# ============================================================

energy = vqe.run(
    qv,
    depth=2,
    max_iter=200,
    mes_kwargs={
        "backend": automatski_backend
    }
)

print("Ground state energy:", energy)


import matplotlib.pyplot as plt

plt.plot(vqe.energy_history)
plt.xlabel("Iteration")
plt.ylabel("Energy (Hartree)")
plt.title("FeMoco VQE Convergence")
plt.show()