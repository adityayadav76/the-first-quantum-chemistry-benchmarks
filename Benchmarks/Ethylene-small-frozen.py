from pyscf import gto
from qrisp import QuantumVariable
from qrisp.vqe.problems.electronic_structure import *

# ============================================================
# Molecule
# ============================================================

mol = gto.M(
    atom = '''
    C 0 0 0
    C 0 0 1.34
    H 0 1 0
    H 0 -1 0
    H 0 1 1.34
    H 0 -1 1.34
    ''',
    basis='6-31g'
)

# ============================================================
# Active Space
# ============================================================

vqe = electronic_structure_problem(
    mol,
    freeze_core=True,
    active_orbitals=14   # 14 orbitals → 28 qubits
)

qv = QuantumVariable(28)

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
# ADAPT VQE
# ============================================================

energy = vqe.run(
    qv,
    ansatz="adapt",
    max_iter=150,
    adapt_pool="uccsd",
    gradient_threshold=1e-3,
    mes_kwargs={
        "backend": automatski_backend,
    }
)

print("ADAPT-VQE energy:", energy)


import matplotlib.pyplot as plt

plt.plot(vqe.energy_history)
plt.xlabel("Iteration")
plt.ylabel("Energy (Hartree)")
plt.title("FeMoco VQE Convergence")
plt.show()