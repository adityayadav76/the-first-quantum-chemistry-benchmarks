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
    active_orb=14       # 14 orbitals → 28 qubits
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
    host="xxx.xxx.xxx.xxx",
    port=xx
)

automatski_backend = AutomatskiBackend(backend=backend)

# ============================================================
# VQE
# ============================================================
vqe.set_callback()

energy = vqe.run(
    qv,
    depth=1,
    max_iter=150,
    mes_kwargs={
        "backend": automatski_backend
    }
)

print("VQE energy:", energy)

vqe.visualize_energy(exact=False)