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
    host="xxx.xxx.xxx.xxx",
    port=xx
)

from AutomatskiBackendQrisp import *
automatski_backend = AutomatskiBackend(backend = backend)

vqe.set_callback()
energy = vqe.run(QuantumVariable(4), depth=1, max_iter=50, mes_kwargs={
        "backend": automatski_backend
    })
print(energy)
#Yields -1.8461290172512965

vqe.visualize_energy(exact=False)