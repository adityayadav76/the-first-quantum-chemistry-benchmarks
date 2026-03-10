from pyscf import gto
from qrisp import QuantumVariable
from qrisp.vqe.problems.electronic_structure import *

mol = gto.M(
    atom = '''H 0 0 0; H 0 0 0.74''',
    basis = 'sto-3g')

vqe = electronic_structure_problem(mol)

# ============================================================
# Run on Automatski Backend
# ============================================================

import sys
sys.path.append('../../python/')
from AutomatskiKomencoQiskit import AutomatskiKomencoQiskit

backend = AutomatskiKomencoQiskit(
    host="XXX.XXX.XXX.XXX",
    port=XX
)

from AutomatskiBackendQrisp import *
automatski_backend = AutomatskiBackend(backend = backend)


energy = vqe.run(QuantumVariable(4), depth=1, max_iter=50, mes_kwargs={
        "backend": automatski_backend
    })
print(energy)
#Yields -1.8461290172512965


import matplotlib.pyplot as plt

plt.plot(vqe.energy_history)
plt.xlabel("Iteration")
plt.ylabel("Energy (Hartree)")
plt.title("FeMoco VQE Convergence")
plt.show()